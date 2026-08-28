# Round306B1AF4K2R2W — R2 W-tail exact-reglue authority audit

## Verdict

`BLOCKED_MISSING_AUTHORITY__FOUR_EXACT_GEOMETRIC_PARTITIONS__ZERO_THEOREM_CREDIT`

The package independently reconstructs the four multiplicity-two R2 W-tail
members from frozen R182, R271 and B1R0 bytes.  All four rational parent/child
box partitions and complete common-face rectangles are exact.  This does **not**
close `ARTIFICIAL_FACE_REGLUE_EXACT_V2`: the frozen B1R0 rows expressly leave
the source-free interval predicate equivalence pending and assign zero full-
support credit, and no sealed authoritative row assigns the artificial face to
one half-open child.  Therefore `r2_artificial_face_reglue_credit=0`.

## Exact four-row frontier

- Member `source-g-expanded-occurrence:777579...f9dc05`: parent leaf
  `round182-collar-leaf:79c940...b0e5e`; children
  `round271-W-tail-side:f685c7...f03c8b` and
  `round271-W-tail-side:8bddfe...81d15`; target `W[1,-1]`; interface
  `t=-47967/128000`; B1R0 union row `round306b1r0-member-union:99effd...faf767`.
- Member `source-g-expanded-occurrence:3dbc14...32a9e0`: parent leaf
  `round182-collar-leaf:24c355...5c086f`; children
  `round271-W-tail-side:283dec...b5943` and
  `round271-W-tail-side:d2ca5b...5a32a9b`; target `W[-2,-1]`; interface
  `t=-47967/128000`; B1R0 union row `round306b1r0-member-union:484739...ed6658`.
- Member `source-g-expanded-occurrence:7679f9...00a231`: parent leaf
  `round182-collar-leaf:2f8300...143b98`; children
  `round271-W-tail-side:7f514e...575380` and
  `round271-W-tail-side:423609...05b05`; target `W[1,0]`; interface
  `t=47967/128000`; B1R0 union row `round306b1r0-member-union:79ee91...0e27e2`.
- Member `source-g-expanded-occurrence:8d341c...1a83819`: parent leaf
  `round182-collar-leaf:272321...6d3f3a`; children
  `round271-W-tail-side:0a7aa9...d704ae` and
  `round271-W-tail-side:9d741d...39c78b`; target `W[-2,0]`; interface
  `t=47967/128000`; B1R0 union row `round306b1r0-member-union:f92565...41d340`.

The full identifiers, exact boxes, source row hashes, cell row hashes, row
commitments and canonical input commitments are in the four-row theorem
ledger; ellipses above are only for report readability.

## What is sealed

- 7/7 input files: held FD, regular single-link path, two pre-parse SHA-256
  passes, post-parse full rehash, final path/FD and directory identity.
- 5/5 complete ordered table commitments: R182 occurrence `54,220`, R182 leaf
  `202,840`, R271 side `70,420`, B1R0 cell `295,340`, B1R0 member `295,336`.
- 4/4 same-parent two-child exact rational interval partitions, complete
  positive-area common `p×s` faces (each area `1/204800`), identical complete
  10-field signatures, target owners and strict-negative region-product signs.
- Four input-bound typed ledger rows.  The row-list digest is
  `378b3f6a45c7f66add5a3396e0ce63ba7ff6cdd5a00cb9d49ef8727219fe7113`;
  result digest is
  `e3231a108032cac6fc0f7c686e18fccbc7b3c48c150542d5c1276578972b7ee0`.
- Independent verifier does not import or execute the producer.  It replays the
  raw tables, uses recursive type-strict equality, rejects `false==0` and
  `true==1`, and rejects 10/10 credit/status/gap/geometry/commitment mutations.

## Exact missing-authority gap

Every ledger row records all four gaps:

1. source-free interval predicate AST and equivalence theorem for both child
   records;
2. a sealed, input-bound whole-face plus two-sided inward-corridor physical
   equivalence certificate;
3. a canonical half-open owner assignment for the artificial interface;
4. an independent receipt for that physical equivalence certificate.

Round278 is useful evidence but remains a nonsealed zero-credit probe: the
workspace has only its source and report, not a result/verification/manifest
package.  K1 is a generic zero-credit checker foundation, not the missing
family-specific theorem.

## Credit boundary

`r2_artificial_face_reglue_credit=0`; normalized support, representation cover,
B1A, B2, maximality and CM2 credits are all zero.  CM2 remains
`NO-GO_FOR_CLAIM`.
