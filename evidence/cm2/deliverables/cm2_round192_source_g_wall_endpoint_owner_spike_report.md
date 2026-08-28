# CM2 Round192 source-G wall endpoint owner spike

## Verdict: PARTIAL

Question: are the 64 Round182 wall-G residual leaves only 32 duplicated
`t=0` source-wall sheets, with a target wall factor that is strictly nonzero,
so that an outcome-blind half-open owner closes the tail?

The boundary pairing part is validated.  The source-only zero-set hypothesis
is invalidated.  The 64 leaves form exactly 32 negative/positive `t` pairs
with byte-identical closed `t=0` faces, and choosing the positive-`t` leaf as
owner gives exactly one owner and one negative-`t` shadow per face.  However,
the target factor is not strictly nonzero on any of the 64 full leaves or
their `t=0` faces.  It has an exact `t=p=0` zero edge in every leaf, and one
side of every pair contains an additional unique clipped target 2D graph.
Consequently each paired wall-product zero set is

`source t=0 sheet ∪ one clipped target sheet`,

not the source sheet alone.  No whole-tube or global credit is justified.

## Frozen input and implementation

- Probe:
  `cm2_round192_source_g_wall_endpoint_owner_probe.py`
- Probe SHA256:
  `f91bf6a6a7b5663d52ceab937d91fa1b7add2e2c72bb992791c83b5b5bdb0d46`
- Schema:
  `cm2.round192.source-g-wall-endpoint-owner-probe.v1`
- Round179 manifest SHA256:
  `8fd5ae3a0cdd0c3321c0f8ffe6183ab57d31088b96523fa41ce0ebbe10d78b76`
- Round179 attachment file/result SHA256:
  `f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42`
  /
  `a5468800c1d89cd307a5a26c608550b04db79c64c562fb12bedb22d6cec308cb`
- Round182 manifest SHA256:
  `32dea92dd0de87d3ded6ed69a908b58b01402ddcdef3f0e2b5ffde096a9383c5`
- Round182 attachment file/result SHA256:
  `ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c`
  /
  `9f0f64d93bd0ac2a9dd41965cbfd95531f07582da5eb4c52f14c44da3d0db269`

The probe pins every entry in both complete manifests, checks both manifest
hashes, recomputes both certificate and verification result digests, requires
both official verifications to be `PASS`, and recomputes both large
attachment result digests.  It imports Round182/Round179 before those pins
can be checked, so this remains a frozen-workspace probe rather than an
adversarial verifier.

`py_compile` passed.  An AST audit found no write-like call or write-mode
`open`; the CLI has no output-path option.  Progress goes to stderr and the
single diagnostic document goes to stdout.

## Full run

Command:

```bash
/usr/bin/time -v -o /tmp/cm2_round192_seed192052.time \
  env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=192052 \
  .venv-neurips/bin/python \
  deliverables/cm2_round192_source_g_wall_endpoint_owner_probe.py \
  > /tmp/cm2_round192_seed192052.json
```

Measured result:

- exit status: `0`
- elapsed: `0:43.53`
- user/system time: `41.64 s` / `1.88 s`
- maximum RSS: `827,956 KiB`
- output file SHA256:
  `277a4866ccfbcb97fcd28d7220d119222a653108816662f91d1fae13a49bb383`
- probe result SHA256:
  `e04efd5a205993e61dbdecca24acbdee0d1056015988b6e394f5c01a10a8ab27`
- 64 leaf evidence rows SHA256:
  `4702ad9ef4a0522d77796924c3ddc5ed075584f887059858d8350b3d81b26492`
- 32 pair evidence rows SHA256:
  `f93a25e1f322bb202c0db99e86357c9b4d7a1940a0ed691a8e508e83a5a9c732`

An independent post-run canonical digest check reproduced the reported probe
result SHA256.

## Exact reconstruction and ownership

- residual wall-G leaves: `64`
- distinct origins: `64`
- face patterns: `S-|U = 32`, `U|S+ = 32`
- negative-`t` leaves: `32`
- positive-`t` leaves: `32`
- one-leaf volume: `177/13107200000`
- total tail volume: `177/204800000`
- exact pairs by
  `(chart, owner_target, wall axis, integer wall, p0, p1, s0, s1)`:
  `32`
- byte/exact common-face matches: `32/32`
- positive-`t` owners: `32`
- negative-`t` shadows: `32`

The policy is outcome-blind: target-factor classification is not part of the
owner key.  Every common face has exactly one positive-`t` owner.

For `G:E` and `G:W`, the relevant source coordinate is `source_y`; for
`G:N` and `G:S`, it is `source_x`.  In all four charts the wall is zero and
the source factor is exactly

`(9/25) t`.

Thus its exact zero set is the common `t=0` source sheet and its `t`
derivative is strictly positive.

## Target-factor obstruction

The proposed strict-target premise fails exactly, rather than merely because
of interval width:

- target factor strict on full leaf: `0/64`
- target factor strict on the common `t=0` face: `0/64`
- exact target zero on the `t=p=0`, variable-`s` edge: `64/64`
- leaves with no off-source target zero:
  `32`
- leaves with one unique clipped target 2D graph:
  `32`
- target graph side: negative `t = 16`, positive `t = 16`

On every leaf the target factor has a strict positive `t` derivative, a
strict signed `p` derivative, and exact zero `s` derivative.  The corner
value at `t=p=0` is exact zero.  When the strict signs on the outer `t` face
and the `t=0`, outer-`p` edge agree, monotonicity leaves only the shared
`t=p=0` edge.  When they disagree, the probe verifies an endpoint bracket,
strict `t` derivative, and interior interval-Newton image on the outer-`p`
edge.  Monotonicity then gives one clipped target graph ending on the
`t=p=0` line.

Each pair therefore has exactly one boundary-only side and one target-graph
side.  Pairing removes duplicate ownership of the source sheet, but does not
remove the target sheet.

## Dimension-safe ledger

- Round179 retained volume for the 64 origins:
  `177/1600000`
- already closed Round182 volume:
  `22479/204800000`
- still-positive wall tail volume:
  `177/204800000`
- exact conservation: yes
- other already closed Round182 leaves: `448`
- deduplicated source 2D sheets: `32`
- additional target 2D sheets: `32`
- source-target 1D intersection segments: `32`
- source-target 0D endpoint incidences: `64`
- source-sheet boundary-edge incidences: `128`
- source-sheet corner incidences: `128`

No 2D, 1D, or 0D stratum is subtracted from 3D coordinate volume.  Newly
credited 3D volume is zero.

The arrangement exposes 96 candidate strict open regions: one region on each
of the 32 boundary-only leaves and two regions on each of the 32 target-graph
leaves.  This is sufficient to say that side-specific local signature
materialization is geometrically feasible, but no signatures were computed
and no original tube was certified.

## Recommendation

Do not formalize this tail as a source-sheet-only boundary glue.  The next
producer should materialize a two-sheet wall-product arrangement for each
pair:

1. one half-open owned source sheet `t=0`;
2. one clipped target graph on its certified side;
3. their exact `t=p=0` intersection segment and endpoint incidences;
4. all 96 side-specific local return signatures;
5. exact dimensional ledgers, attachment rows, attacks, cold replays, and an
   independent verifier that treats the producer as inert bytes.

Until that work is complete, the strict state remains:

- whole original tubes certified here: `0`
- source-G global dispositions: `0/224580`
- Gate5: `10/18`
- D02: `BLOCKED`
- CM2: `NO-GO`
