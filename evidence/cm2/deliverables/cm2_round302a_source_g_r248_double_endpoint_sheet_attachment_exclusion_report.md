# Round302-A R248 double-endpoint sheet attachment exclusion

## Outcome

Round302-A closes the 32 `ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET` rows that
Round300-C withheld and Round300-E did not audit.  All 32 are fail-closed
for occurrence-component attachment:

- 16 complete Round236 double-endpoint partitions produce exactly two sheets
  each, one for `source` and one for `target`;
- the 32 sheets have 16 distinct owner-bulk nodes and all 32 sheet-owner
  pairs are already internal to one pinned Round266 base component;
- the complete 55,428-row Round291 physical frontier contains zero cells
  sharing the required retained child and source chart with any selected
  sheet, hence there are zero exact/equal or positive-area base candidates;
- the complete 113,452-row Round295-A physical binding frontier therefore
  contributes zero occurrence attachment candidates;
- the complete 6,322-row Round300-C witness frontier has zero direct sheet
  witnesses.

Eight of the 16 owner bulks have one Round300-C positive-volume witness.
Those eight rows are retained as context only.  Bulk connectivity cannot be
transferred to a two-dimensional sheet as occurrence attachment credit.

## Exhaustion boundary

The legal graph attachment predicate used by Round300-E is reopened
fail-closed: matching retained child and source chart are mandatory before
exact base, predicate equation, and owner signature/key can be considered.
Here the first-stage candidate count is already zero, so no later predicate
can be bypassed.

The output ledger has 32 self-closed rows, zero unresolved sheets, zero
DSU-eligible edges, and zero component, identity, rank, maximality, fibre, or
global-disposition credit.

## Independent verification

The verifier reconstructs every expected row before opening candidate
artifacts and treats the producer only as the fixed byte string
`8b1feab487ea333ccdfce3051db623f303b674d8dccc5ac36039208ca4e8171f`.
It rejected 46/46 attacks: 32 fully reclosed semantic attacks and 14 strict
JSON/GZIP/path attacks.

Two producer seeds and two verifier seeds reproduced identical bytes:

- producer result self-closure:
  `c2b94b7993334886e80060fe607d315c8e59eb8ec174ae5047e949a0c359c7fa`;
- ledger rows:
  `75dbc01a8b58ee41bc17b08f414b29cb82254b293024334614785abcfb216c9b`;
- verification self-closure:
  `c294b46739228de648779dca5af9e41fdae04d9902c078aeab44b3609cc646ef`;
- attack-suite self-closure:
  `e30c7115f48a1f5fe9e0677b1ba6d744c3358f85f34a6aa65bd10b1f5f449b2e`.

## Strict nonclaim

Round302-A is an exclusion gate.  It does not add an edge or modify the
Round301 component partition.  Component maximality remains a separate gate
that must consume this sealed exclusion together with all other legal and
ineligible frontiers.
