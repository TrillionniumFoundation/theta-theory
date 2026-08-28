# CM2 Round182 — source-G clipped graphs and pair arrangements

Date: 2026-07-26  
Verdict: `CERTIFIED_BOUNDED_PARTIAL_SOURCE_G_CLIPPED_GRAPH_AND_PAIR_ARRANGEMENT__NO_GLOBAL_EXACT_KEY_DISPOSITION_OR_D02_PROMOTION`

## Frozen input and scope

Round182 pins the byte-identically replayed Round179 certificate, row
attachment, verifier, verification, and manifest.  The Round179 attachment
contains 62,012 Round174 residual origins.  Round179 had already completely
replaced 4,116 of them; Round182's positive-volume input is therefore exactly
the 106,680 retained children of the remaining 57,896 original tubes, with
coordinate volume

`1768407/524288000`.

The distinction between original tubes, predicate occurrences, local
return-key observations, and global source-G exact-key fibres is enforced in
every table.  No Round182 row carries global disposition credit.

Frozen Round182 producer:

- source SHA256:
  `8638f2722e68bd5c6e0eb5932dc76780728998f21a47b1d8c02c28449e984d56`
- certificate file SHA256:
  `27491e3943e88772ec15cee110cd983b14ad82a2a56f8a07d605c3cd8fb49f08`
- certificate result SHA256:
  `e07da794eed6dbb404de8913f5b871621f9f1b59b355172a37192791ae28911d`
- attachment file SHA256:
  `ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c`
- attachment result SHA256:
  `9f0f64d93bd0ac2a9dd41965cbfd95531f07582da5eb4c52f14c44da3d0db269`
- attachment byte count: `158,815,476`

## Occurrence census and bounded collar method

Round179's full occurrence census has 30,444 outgoing face-overwrap rows and
23,776 wall face-overwrap rows.  Of those, 284 outgoing and 112 wall
occurrences belong to original tubes already completely replaced by
Round179; they remain inert occurrence records with zero retained-volume
input.  The active Round182 census is therefore:

- active outgoing collars: `30,160`
- active wall collars: `23,664`
- active collars on partial origins: `53,824`
- inactive occurrences on already-replaced origins: `396`
- total occurrence ledger: `54,220`

There is at most one active face-overwrap occurrence per partial original
tube.  The two occurrence families do not overlap.

For every retained child, the verifier rebuilds the predicate on the two
`t` faces.  A zero graph is claimed present only when the face signs bracket
zero and a strict interval derivative gives uniqueness.  A strict derivative
without a bracket is never treated as existence.

- G-target outgoing and G-target wall collars use the strict `t` derivative
  and parametric `p` face normal form, with at most six `p` splits for a new
  internal Round179 child face.
- W-target outgoing collars use the strict `t` derivative and at most six
  dyadic `s` splits.  The remaining unresolved base boxes stay positive
  3-dimensional collars.
- Every leaf carries an exact rational box, coordinate volume, base
  coordinate area, lower/upper face status, and separate 3D/2D/1D/0D counts.

The bounded leaf census is:

- total collar leaves: `202,840`
- closed leaves: `184,452`
- residual 3D collar leaves: `18,388`
- full-base 2D graph leaves: `12,332`
- clipped 2D graph leaves: `99,192`
- empty graph leaves: `72,928`
- 2D graph sheet cells: `111,524`
- 1D clipping-curve segments: `122,160`
- 0D clipping endpoint incidences: `244,320`

Exactly `19,716` leaves have clipping curves on both `t` faces.  Both curves
use the same `p` graph axis in every row (`axis_mismatch=0`).  The strict
whole-box `t` derivative prevents the two face curves from intersecting and
orders them, so each such leaf contains one clipped 2D sheet bounded by two
1D curves—not two sheets and not a crossing.

## Exact 3D conservation

Round182 closes 49,564 of the 57,896 partial original tubes as local
geometric cell complexes.  It leaves 8,332 original tubes with a positive
3D residual.

- closed retained coordinate volume:
  `282700329/83886080000`
- residual retained coordinate volume:
  `244791/83886080000`
- their sum:
  `1768407/524288000`

The 2D graphs, 1D clipping curves, and 0D endpoint incidences are kept in
separate ledgers and are never subtracted as 3D volume.

“Fully geometrically replaced original tube” is a local cell-complex claim.
It is not an exact-key-fibre disposition and does not promote Gate5 or D02.

## The 336 pair arrangements

All pair origins have a G target and one exact source integer-wall graph.
Round182 asserts the source factor symbolically:

- source charts `G:E` and `G:W`:
  `source_y=(9/25)t`, wall axis `Y`, wall `0`;
- source charts `G:N` and `G:S`:
  `source_x=(9/25)t`, wall axis `X`, wall `0`.

Thus the source graph is exactly `t=0`, with exact derivative `9/25`.
The fixed 2×2 Jacobian minor is the product of this exact factor and the
strict `p` derivative of the second predicate.  A nonzero minor proves
transversality only; existence is independently proved by opposite strict
`p`-face signs and a strict-interior interval-Newton self-map.

The complete result is:

- `112` unique transverse 1D intersection lines;
- `216` empty intersections by strict same-sign `p` faces;
- `8` empty intersections because one entire predicate has an empty zero
  set;
- `112` strict-interior interval-Newton inclusions;
- `224` isolated boundary 0D endpoint incidences, two for each actual line.

Every pair row lists the strict endpoint intervals, derivative interval,
exact source factor, strict Jacobian-minor interval, Newton domain/image, and
the unique Round179 retained child incident to `t=0`.  Every endpoint is an
incidence row, not a globally deduplicated component count.

## Source-chart seam ownership

The 472 source-chart seam rows retain the exact equation
`2*t^2-1=0`, strict derivative, and opposite `t`-face signs.

- `236` `E/W` rows are the half-open owners;
- `236` `N/S` rows are excluded shadow copies.

This resolves chart ownership locally without generating any source-G
global exact-key disposition.

## Independent verification and hardening

The independent verifier SHA256 is

`790b17cf6dadebc37b889fff63c6ecde985cccf53c95523cd6c2bc39d12db566`.

It imports only the pinned Round179 independent-verifier evaluator.  The
Round182 producer is pinned as inert bytes and is never imported or executed.
The verifier independently reconstructs all seven row tables, all
`158,815,476` attachment bytes, every table digest, the complete certificate,
and the complete expected certificate/attachment canonical equality.

Seed 17 result:

- verification result SHA256:
  `61715ef39e232937d821ba1c634181f905454b758abbe98d889c768ddc809797`
- verification file SHA256:
  `b008c2208891374696b88506e87957bbb754d95d62677d9406c466405b311f36`
- elapsed: `26:54.04`
- maximum RSS: `2,148,492 kB`
- semantic mutations with all affected digests re-signed: `36/36` rejected
- strict JSON/oversize attacks: `10/10` rejected
- path/type/output-alias/prepositioned-temp attacks: `12/12` rejected

The semantic suite explicitly attacks producer provenance, 8,332 residual
origins, both-face curve ordering, pair existence/Jacobian separation,
0D-incidence versus component semantics, source-seam ownership, Gate5, D02,
CM2, and the global `0/224580` disposition count.

Input and output path checks use `abspath` without resolving the final path,
`lstat`, single-link regular-file requirements, and exact parent resolution.
Atomic writes use `mkstemp`/`O_EXCL`, `fsync`, and `os.replace`; prepositioned
temporary symlinks are never followed.

Cold replay is byte-stable:

- producer seed `211`: certificate and the complete `158,815,476`-byte
  attachment are byte-identical to the frozen formal artifacts; elapsed
  `14:52.90`, maximum RSS `1,339,732 kB`;
- verifier seed `211`: byte-identical to seed `17`; elapsed `27:11.79`,
  maximum RSS `2,146,924 kB`;
- parent verifier seed `182051`: independently byte-identical; elapsed
  `27:26.64`, maximum RSS `2,148,824 kB`.

The full commands, hashes, and comparisons are recorded in the cold-replay
note.

## Global state and next core gate

Round182 issues no global promotion:

- source-G global geometric dispositions: `0/224580`
- Gate5: `10/18`
- complete global 18-field blocks: `0`
- open fields: `F5,F6,F10,F11,F14,F15,F17,F18`
- D02: `BLOCKED`
- D03 negative oracle: `UNAUTHORIZED`
- CM2: `NO-GO`

The next source-G gate is to resolve the 18,388 bounded residual W-target
and wall collar leaves (8,332 original tubes; 928 Gate3 parents; 12,024
retained-child IDs; volume `244791/83886080000`) and then materialize
side-specific local return signatures.

An independent join using
`leaf.occurrence_row_id = collar.Round179_occurrence_row_id` gives:

- `18,324` outgoing-W residual leaves on `8,268` origins;
- `64` wall-G residual leaves on `64` origins;
- the 64 wall-G face patterns are exactly `S-|U` (`32`) and `U|S+` (`32`);
- outgoing-W has only `88` true `U|U` leaves; the other `18,236` have one
  unresolved face and one strict analytic face.

The next bounded continuation should therefore split
`normal_x^2-normal_y^2` into the two factors
`h+=normal_x+normal_y` and `h-=normal_x-normal_y`, certify centered C0/C1
forms and one-sided `t`-face brackets factor by factor, and exclude a
simultaneous factor zero from nonvanishing of the target normal.  It should
handle the 18,236 one-sided outgoing-W leaves first, isolate the 88 `U|U`
leaves, and keep the 64 wall-G leaves as a separate tail.

A global disposition remains forbidden until every return signature in an
entire source-G exact-key fibre is covered or excluded.
