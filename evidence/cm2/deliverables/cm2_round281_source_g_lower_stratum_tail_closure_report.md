# CM2 Round281 — source-G lower-stratum tail closure

Status: **PASS_INDEPENDENT_ROUND281_LOWER_STRATUM_TAIL_CLOSURE — ZERO CREDIT**

Round281 closes the 1,276 nonterminal rows left by the Round280 lower-stratum
probe.  It is a local physical-support decision certificate only.  It creates
no expanded occurrence, component edge, maximality result, exact-key fibre
result, global disposition, or `Jx/Jy` same-point identification.

## Exhaustive result

- 880 exact source-factor `t=0` rows:
  - 440 positive-`t` half-open owners;
  - 372 negative-`t` rows fully shadowed by positive owners;
  - 60 negative-`t` rows absent from the complete 21,232-row Round174
    unique-first positive-owner universe;
  - 8 negative-`t` rows split exactly into a positive-owner shadow cell and
    an absence cell.
- 396 fully-replaced Round179 origins:
  - all have exactly two resolved `p`-children;
  - retained and guard child counts are zero;
  - the two child volumes exhaust the origin volume;
  - strict outgoing-dominance signs or strict wall-factor pairs exclude the
    nominal support throughout both children.

The eight mixed rows were not promoted to whole-row shadows.  Each original
face has area `1/12800`, with exact owner coverage `1/25600` and exact
complement absence `1/25600`.  The complement was checked against every
positive-`t` Round174 parent in the corresponding chart.

Global `t=0` area conservation is exact:

- total face area: `31/640`;
- owner or shadow area: `59/1280`;
- absence area: `3/1280`;
- partition delta: `0`.

Combining Round281 with the already frozen Round280 terminal rows gives the
complete 55,428-row lower-stratum local disposition:

- 39,252 whole physical-support rows;
- 16,168 whole absence rows;
- 8 explicitly partitioned physical/absence rows;
- 0 formal-provenance-only rows;
- 0 unresolved local physical decisions.

This count is not the 224,580 global exact-key disposition gate and does not
change that gate's zero-credit status.

## Replay and verification

The producer was cold-replayed with seeds `281071` and `281929`.  The ledger
and result bytes were identical.  The deterministic gzip stream passed
`gzip -t`.  Six producer-side mutation attacks were rejected.

The independent verifier does not import the Round281 producer.  It rebuilds
all 880 face partitions from the frozen Round174/179 universe, recomputes all
396 exhaustive resolved-child covers and strict signs, checks every row hash,
and reasserts all zero-credit fields.  Its status is
`PASS_INDEPENDENT_ROUND281_LOWER_STRATUM_TAIL_CLOSURE__ZERO_CREDIT`.

## Strict baseline after Round281

- quotient: 63,224;
- expanded occurrences: 126,468;
- maximality: 0/63,224;
- exact-key fibres: 0/116;
- global dispositions: 0/224,580;
- Gate5: 10/18;
- D02: BLOCKED;
- CM2: NO-GO_FOR_CLAIM;
- `Jx/Jy` same-point glue credit: 0.

The next core gate remains analytic incidence: construct explicit seam-normal
corridors for the 152 true-seam patches, disposition the 13,788 R275 rechart
regions as exact aliases/new disjoint regions/partial overlaps, then freeze the
final occurrence identity and DSU quotient.

