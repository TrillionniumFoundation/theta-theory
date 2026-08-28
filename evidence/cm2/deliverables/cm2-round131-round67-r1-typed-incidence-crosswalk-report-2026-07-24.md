# CM2 Round 131 — Round67/R1 typed-incidence crosswalk report

Date: 2026-07-24

Round 131 freezes a fail-closed audit, not a new nonempty common root.

The frozen chain contains 64 Round28 moving first-event grazing occurrence
seeds and 128 oriented hit/miss trace seeds.  Round69 proves that their
strict-inner R1 typed incidence is empty.  Separately, Round71/72 contains 32
nonempty stationary terminal-core-preimage components, 64 one-sided traces
and 32 numeric F10/F13/F16 rows on 16 base-R1 path cells.  Those terminal
components are not occurrence-pullback faces.

The Round67 physical fixed-time root is certified at the standard-Borel
theorem level, but it exports no materialized recordwise rows carrying the
required twelve-field key:

`restriction_id, return_component, insertion_time, collision_index,
event_signature, primitive_key, owner_key, rank_zero_component, plaque_side,
word_cell, endpoint_coordinate, root_coordinate`.

Consequently the certified Round131 crosswalk has:

- 0 typed-incidence match rows;
- 32 explicitly unmatched Round72 component rows;
- 12 unmatched required-field rows;
- 2 carrier-type rows;
- 6 obstruction rows;
- 53 total closed rows.

Every unmatched component remains pinned to `s=0`, return depth 1, roof level
0, its exact component/core/path/word IDs, two traces and numeric
F10/F13/F16 attachment.  None is retyped as a Round67 owner record.

The first direct carrier-compatible target not already ruled out is a
nonempty occurrence-pullback component on an `R_n` path with `n>=2`, together
with a deterministic Borel graph from exact Round67 endpoint/root coordinates
to physical `(s,t,p)` coordinates.  A later separate quotient would still be
needed to attach the existing Round72 terminal-preimage numeric rows.

Global safety remains unchanged:

- Gate5 global maturity: `10/18`;
- global complete 18-field blocks: `0`;
- Gate5 blocks: `0`;
- Gate5: `NOT_CERTIFIED`;
- CM2: `NO-GO_FOR_CLAIM`.

The independent verifier does not import or execute the Round131 producer.  It
reconstructs the 24 physical cores, the four-way Round71/72/128 component
join, the Round28/Round67/Round69 carrier obstruction, and all 53 rows.  It
rejects 45 re-signed semantic mutations and 18 strict-JSON attacks.
