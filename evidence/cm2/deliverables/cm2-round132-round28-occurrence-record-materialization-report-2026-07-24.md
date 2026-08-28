# CM2 Round 132 — Round28 occurrence-record materialization report

Date: 2026-07-24

Round 132 materializes the finite source-side data that Round28 constructed
but did not emit.  It independently rebuilds 64 genuine moving first-event
grazing occurrence-face records from the frozen maximal-row/current,
boundary-recovery-carrier and all-scale-parameter-germ sources.  Each face has
one hit and one miss trace, giving 128 oriented traces.

The twelve-field Round67 source schema is:

`restriction_id, return_component, insertion_time, collision_index,
event_signature, primitive_key, owner_key, rank_zero_component, plaque_side,
word_cell, endpoint_coordinate, root_coordinate`.

Nine fields have canonical source-side representations with explicit typed
qualifiers.  This is not a nine-field owner/path join:

- `plaque_side` is only the oriented hit/miss trace carrier; every trace has
  `stable_plaque_side_claimed=false`;
- `word_cell` is an occurrence word cell derived from the physical label; its
  official return-path word ID is null;
- endpoint and root coordinates are exact local source descriptors, not an
  endpoint/root-to-`(s,t,p)` path map.

The three missing fields remain `return_component`, `owner_key` and
`rank_zero_component`.  No Round67 owner map `q_j`, owned `Omega_j` record,
occurrence-pullback component, exact path-coordinate map or typed-incidence
match is materialized.  Thus the source-side status is `9/12`, while the
joined owner/path status remains `0/12`.

The closed finite ledger is:

- 64 occurrence-face rows;
- 128 oriented trace rows;
- 12 field-status rows;
- 0 typed-incidence match rows;
- 4 obstruction rows;
- 208 total rows with 208 unique row hashes.

The independent verifier does not import or execute the Round132 producer.
It reconstructs all 64 faces, all 128 traces and all 208 rows from the pinned
lower-level sources, recovers the frozen Round28 registry digests, and checks
every row, group and outer closure.  It rejects 58 re-signed semantic
mutations and 18 strict-JSON attacks.

The first unruled-out direct target remains a nonempty occurrence-pullback
component on an `R_n` path with `n>=2`, followed by owner materialization and
an exact Borel endpoint/root-to-path-coordinate map.

Global safety is unchanged:

- Gate5 global maturity: `10/18`;
- global and complete 18-field blocks: `0`;
- Gate5 blocks: `0`;
- Gate5: `NOT_CERTIFIED`;
- CM2: `NO-GO_FOR_CLAIM`.
