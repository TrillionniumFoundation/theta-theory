# CM2 Round144: Round137-v1 superseding migration schema

Date: 2026-07-24

## Result

Round144 certifies an append-only, fail-closed migration domain rooted in
`round137-dyadic-basis-enumeration-v1`.  It freezes six disjoint prospective
identifier namespaces and a 14-node dependency DAG without reinterpreting or
aliasing any historical Round27/35/50/54/67 identifier.

The certified status is:

`CERTIFIED_VERSIONED_SUPERSEDING_MIGRATION_SCHEMA__NO_CORRECTED_COMPONENT_MINTED`

The registry is:

`round144-round137-v1-migration-registry:c976f6db9ccec006c82e87cb319f699e11b362e8a1fb4d4357c5f17beb17de1a`

## Frozen prospective namespaces

Each identifier has the serialization

`prefix + ":" + sha256(canonical_JSON_array([namespace_version, ordered_payload_values]))`.

The six prefixes are:

1. `c24v1-component`
2. `rn-v1-parent-W`
3. `rn-v1-restriction`
4. `round50-v1-owner`
5. `round54-v1-t54`
6. `round67-v1-qj`

They are distinct from the historical `c24-component`, `rn-parent-W`, and
`rn-restriction` domains.  If any ordered payload field or direct prerequisite
is absent, the identifier is null and must not be minted.

## What migrated mechanically

Eighteen rows are copied from byte-pinned Round137/140/142 evidence:

- the Round137-v1 enumeration ID, zero-based origin, and executable 1D/2D row
  contracts;
- source core
  `core:90398e9ab632e57b027266bc7c34461a0a6a6d308c35fbeacc41432a3d7f48f7`;
- return depth 1648;
- exact path tuple SHA256
  `5cec1061ec331e8f37929dfb1b2b2a78757309ba60198d571abd9e8cf6c70ed9`;
- 1,648 official word occurrences, 141 unique words, and the official sequence
  SHA256;
- exact `s=0` and the implicit exact `b_star` descriptor;
- the incidence path `[14] x 1648`, its SHA256, and `delta_14=1/8388608`;
- the Round140 adaptive seed-cell ID and set-theoretic containing-component
  locator;
- the contained 2D and 1D Round137-v1 basis rows as positive upper bounds;
- the Round142 historical-enumeration underdetermination proof ID.

The contained 2D row is at level 5883 and has rank digest
`81ee4f795045d8478e621dbcaf2cba2437ccb168b34b770f995c012c0060927f`.
It remains an upper bound, not a least component rank.  The contained 1D row
is also at level 5883 and has rank digest
`fe02c53ca61c7ae9a81d189ffbf5d58cbae33ee16cb68e6248c65d5fc708c24d`;
it is not asserted to rank the full leaf interval.

## Exact migration frontier

Only DAG nodes D00 (adopt Round137-v1) and D01 (pin the R1648 seed payload) are
ready.  The first exact blocker is D02:

`a complete validated two-generator centered-jet outer atlas with exhausted event frontier`

After D02, D03 must exclude every earlier Round137-v1 basis row from closure
containment in the maximal component.  Only then may D04 mint a prospective
component ID.

The remaining order is:

- exact full leaf interval and 1D leastness/short-cell proof;
- prospective parent-W ID;
- exact image recut and prospective restriction ID;
- the Round132-to-Round50 17-field active-representation crosswalk and complete
  same-event fibres;
- prospective owner ID;
- same-root Round54 word/side/endpoint serialization and prospective t54 token;
- typed `Omega_j` record and recordwise `q_j` serialization.

The future-certificate acceptance contract allows formally pinned
centered-affine and leaf-endpoint/image-recut certificates to fill only their
guarded DAG nodes.  A centered collar alone does not close D02; a leaf
endpoint certificate alone does not close D04.

## Current null ledger

The following remain null:

- least 2D rank of the maximal component and `component_v1_id`;
- least full-leaf 1D rank, natural short-cell `k`, and `parent_W_v1_id`;
- image-recut v1 rank and `restriction_v1_id`;
- active-representation crosswalk and `owner_v1_id`;
- `t54_v1_token`, typed `Omega_j` record, and `q_j_v1_output`.

No corrected component ID is minted.  No historical rank or ID is recovered.

## Independent verification

The independent verifier does not import or execute the producer.  It
reconstructs:

- 6 namespace rows;
- 14 DAG rows;
- 18 mechanically migratable rows;
- 12 unavailable-field rows;
- the 17-field Round133 owner replacement contract;
- the D02 first blocker and the all-null identifier ledger.

It rejected 34 semantic mutations, 8 strict-JSON attacks, and 12 in-process
path attacks.  Seventeen hostile process/I/O cases all exited 1, created no
unexpected output, left symlink/hardlink targets unchanged, and preserved all
pinned bytes.

Dual-hash-seed producer outputs are byte-identical to the frozen certificate.
Dual-hash-seed verifier outputs are byte-identical to the frozen verification.
Atomic replacement of an existing sentinel changed the output inode.

## Strict status

- Historical Round27 component rank/ID: not recovered.
- New versioned component/parent-W/restriction/owner/token/output IDs: 0.
- Global complete 18-field blocks: 0.
- Gate5: `10/18`, `NOT_CERTIFIED`.
- CM2: `NO-GO_FOR_CLAIM`.

