# CM2 Round 133 — Round132 owner-map realizability audit

Date: 2026-07-24

Round 133 freezes a fail-closed owner-map audit.  It does not construct a new
owner row.

The frozen chain contains two different operations that must not be
conflated:

1. Round 50 selects the lexicographically least active primitive inside one
   complete, primitive-free physical-event fibre.
2. Round 61/67 declares a deterministic Borel map `q_j` on the already-owned
   domain

   `Omega_j={(a,x):x in E_(j,a)^owner intersect R_(j,a)^reg}`.

The target of `q_j` is the standard-Borel Round54 owner/root base retaining
the full `t54` token and endpoint/root coordinates.  The frozen artifacts
declare that map and its same-law pushforward, but provide no executable
recordwise formula, serialized graph row, or canonical `owner_key` encoding.
Round54's dyadic collar selector and Round60's
`pi_50(t54)=drop(word-cell)` projection are not `q_j`.

Round132 materializes 64 genuine moving-occurrence source records.  For every
record, its Round132 event digest explicitly contains the primitive key.
Consequently the 64 distinct event digests separate primitive
representations; they do not form the primitive-free Round50 fibres needed
for owner minimization.

Each of the 64 source rows also lacks:

- a parent-`W`, arbitrary-`R_n` path and canonical component;
- membership in `E_i` and `R_i^reg`;
- a complete same-event active primitive fibre;
- a connected rank-zero root witness;
- a hit/miss-to-minus/plus side reconciliation;
- a same-root Round54 word cell;
- a recordwise `q_j` output and canonical owner key.

Therefore the certificate contains:

- 64 closed owner-candidate request rows;
- 5 ordered blocker rows;
- a 17-field minimum replacement contract;
- 86 finite closed rows in total;
- 0 certified or materialized Round67 owned records;
- actual nonempty owned-subset existence:
  `UNKNOWN_NOT_CERTIFIED`.

The first missing object is the Round132-to-Round50 active-representation
domain crosswalk.  A legal next construction must materialize one complete
primitive-free event fibre on a particular path/component/parent curve,
prove regular activity and its unique transverse rank-zero root, select the
least primitive, reconcile the side and word-cell fields, and only then
encode the `q_j` output.

The independent verifier does not import or execute the Round133 producer.
It independently checks the Round50/54/58/60/61/67 contracts, rebuilds every
Round132 event digest and all 86 Round133 rows, and rejects 90 re-signed
semantic mutations and 19 strict-JSON attacks.  The mutations include:

- replacing `UNKNOWN_NOT_CERTIFIED` by an empty-set claim;
- selecting any of the 64 observed rows as a lexicographic minimum;
- using a tangent target, core label or occurrence ID as an owner;
- inventing a recordwise `q_j` formula;
- renaming hit/miss or occurrence word cells as Round50/54 fields;
- promoting a typed match, global complete block, Gate5 or CM2.

Global safety is unchanged:

- Gate5 global maturity: `10/18`;
- global complete 18-field blocks: `0`;
- Gate5 blocks: `0`;
- Gate5: `NOT_CERTIFIED`;
- CM2: `NO-GO_FOR_CLAIM`.
