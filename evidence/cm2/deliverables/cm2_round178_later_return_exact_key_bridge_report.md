# CM2 Round178 — later-return exact-key bridge

Date: 2026-07-26

## Verdict

`PARTIAL`, with no Gate5, D02, whole-stratum, or whole-parent promotion.

The collision-1 coordinate bridge is globally closed on all 16 strict-live
Round177 strata.  Collision 2 is only boundedly resolved on strict 3D inner
boxes: 0/16 live strata are fully closed and 16/16 remain partial.  D02
therefore remains `BLOCKED`, Gate5 remains `10/18`, and CM2 remains
`NO-GO_FOR_CLAIM`.

Round177 and its frozen artifacts were not modified.

## Global collision-1 bridge

The source is `W[0,0]`; the first selected target is `W[1,0]`; the recentering
removes deck shift `(1,0)`.  With

`eta = cross(u0, center(W[1,0]) - q0)` and
`Delta = (4/25)^2 - eta^2`,

the post-collision normal is

`n1 = (-sqrt(Delta)u0_x + eta u0_y, -sqrt(Delta)u0_y - eta u0_x)/(4/25)`.

The exact next-source Gate3 coordinates are

`(t1,p1,s1) = (n1_y, eta/(4/25), s)`

on strict outgoing chart `W`, where `-n1_x > |n1_y|`.  The compact bridge is

`q1 = eta/(4/25 + sqrt(Delta))`,
`z1 = -n1_y/(1 - n1_x)`,

with exact inverse relations

`p1 = 2q1/(1+q1^2)` and `t1 = -2z1/(1+z1^2)`.

This binds the Round162 compact/Gate3 bridge, the Gate3 candidate registry,
deck recentering, the unchanged `s`, and the half-open `W` diagonal owner.
No dynamical disposition is inferred from the coordinate bridge itself.

## Adjacent-chart guards and lower-dimensional strata

The two Round177 source-chart guard slices are recharted without loss or
duplication:

- `W:E:00.15.0000000` uses adjacent `W:S`;
- `W:E:07.00.1111111` uses adjacent `W:N`.

The exact rechart is

`t_adj = sqrt(1-t_E^2), p_adj = p_E, s_adj = s_E`,

with Jacobian determinant `-t_E/sqrt(1-t_E^2)`.  It is strictly nonzero on
the open guard slices and has selected-seam values `+1` and `-1`,
respectively.  The 2D diagonal seam is owned by `E`; the adjacent `N/S`
representations exclude it.

The ledger counts each of the two physical 2D source seams once and counts
the four 1D seam intersections (`2 × Delta`, `2 × H`) once.  It retains
18 Delta graph pieces, 18 H graph pieces, and 14 H parent-face clipping
rows.  All lower-dimensional integer credit is zero.

## Bounded collision-2 ledger

The exact parent volume is `11151/204800000`.  The two-phase adaptive
partition has 13,692 terminal 3D boxes and exact volume conservation.

| Terminal status | Boxes | Exact volume |
|---|---:|---:|
| `COLLISION1_DELTA_ROOT_COLLAR` | 276 | `51507/3276800000` |
| `COLLISION1_OUTGOING_CHART_COLLAR` | 172 | `122307/13107200000` |
| `COLLISION1_ROOT_ORDER_COLLAR` | 50 | `177/524288000` |
| `COLLISION2_CANDIDATE_ROOT_ORDER_COLLAR` | 11,416 | `10040679/13421772800000` |
| `COLLISION2_EXACT_KEY_RESOLVED` | 1,360 | `842697/13421772800000` |
| `COLLISION2_WALL_OR_CORNER_COLLAR` | 158 | `177/6710886400` |
| `SOURCE_CHART_SEAM_COLLAR` | 32 | `177/409600000` |
| `STRICT_NOT_LIVE_EARLIER_COMPETITOR` | 8 | `531/6553600000` |
| `STRICT_NOT_LIVE_OUTGOING_MISMATCH` | 116 | `21417/3276800000` |
| `STRICT_NOT_LIVE_OWNER_ABSENT` | 104 | `8673/409600000` |

Only six parents contain any strict resolved collision-2 inner boxes:

| Parent | Resolved 3D boxes | Local official ordinals |
|---|---:|---|
| `W:E:00.14.01101` | 122 | 291560, 322097 |
| `W:E:02.11.110` | 40 | 291560 |
| `W:E:05.04.001` | 40 | 290575 |
| `W:E:07.01.10010` | 122 | 290575, 321111 |
| `W:N:05.00.00100110` | 518 | 291560 |
| `W:S:H.05.00.00100110` | 518 | 290575 |

The other ten parents are all-collar at this bounded depth.  Neither the six
parents with inner boxes nor the ten all-collar parents are declared closed.

The strict 3D inner-box key set is:

- ordinal 290575:
  `gate5-word:290575:5e5950ce63693dc08790f017f8e5cc79eb8aa776ff4c53c10a60b27a161178b2`;
- ordinal 291560:
  `gate5-word:291560:6c7c484df06c7e03aef7e83aa2fe403090d4843175262deb78c507154f349115`;
- ordinal 321111:
  `gate5-word:321111:3999d72b42e3b63c9af39dd436e61b7ad9b8176021d87998c93bcaec67fbd2fd`;
- ordinal 322097:
  `gate5-word:322097:a2499191a9e06bd2a47e12fff99af0cc7eb929f04e7c801188cca91e8304d5de`.

The 16 point witnesses observe four distinct local ordinals:
289591, 291560, 321111, and 322097.  In particular, 289591 is point-observed
only, while 290575 occurs on strict inner boxes but is not in the distinct
point-observed set.  Neither kind of occurrence is a global Gate5
disposition.  The official registry remains
`448 × 985 = 441280` keys with digest
`841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9`.

## Independent verification

The verifier does not import or execute the Round178 producer.  It decodes
the 16 parents from the pinned Gate3 atlas and independently reconstructs
all 13,692 terminal rows, collision owners, wall orders, outgoing charts,
official Gate5 keys, exact counts, and exact volumes.  Acceptance requires
full canonical equality with that rebuilt result.  No frozen expected-result
digest is used as the semantic rejection shortcut.

Verification is `PASS`:

- full independently rebuilt result equality: yes;
- re-signed semantic mutations rejected: 26/26;
- strict JSON attacks rejected: 9/9;
- path/alias attacks rejected: 11/11.

The semantic suite explicitly covers point-observed 289591 promotion,
inner-box 290575 promotion, six-parent and 16/16 promotion, each of the ten
all-collar parents, zero/wrong-sign Jacobians, changing the `E` seam owner,
duplicating/omitting 1D rows, exact total/status-volume/count mutations, and
forged D02/whole-parent credit.  Every semantic mutation recomputes the
top-level result digest before validation.

The effective Arb precision is 384 bits.  It is not manually raised by
Round178: the pinned atlas initializes 192 bits, then the fixed, pinned
registry transitive import chain raises the shared context to 384 bits.
The verifier pins both precision-raising source files and verifies their
hashes against the pinned registry's embedded dependency hashes.

Producer and verifier were each replayed under `PYTHONHASHSEED=1` and
`PYTHONHASHSEED=987654321` with the same import order.  Both pairs were
byte-identical.

## Next core gate

Replace the finite Delta/H/root/wall/chart collar outer by parametric
interval-Newton graph cells and exact wall-order arrangements until all 16
collision-2 live strata are closed.  No D02 re-audit is authorized before
that closure.
