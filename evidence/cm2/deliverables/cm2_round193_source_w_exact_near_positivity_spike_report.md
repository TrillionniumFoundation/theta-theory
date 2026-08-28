# CM2 Round193 — source-W exact-near-positivity spike

Date: 2026-07-26  
Verdict: `INVALIDATED`

## Question

Can the exact Round187 depth-2 source-W clipped tail be closed by replacing
the coarse sufficient condition

`ell - target_radius > 0`

with the exact near-root conditions on the `Delta >= 0` strata,

`ell > 0` and `ell^2 - Delta > 0`?

The second condition is preferably recomputed as

`distance_squared - target_radius_squared > 0`,

then cross-checked against the independent `ell^2 - Delta` interval
enclosure.  TAU and competitor order must be replayed cell by cell; the
64 full-p cells remain a separate holdout.

## Frozen probe and command

The read-only probe
`cm2_round193_source_w_exact_near_positivity_probe.py` is frozen at SHA256

`fca55b9f9a28aeda65f2e4a5a2305e704f198b3f08d10891fe607f46273f3a52`.

Before importing any probe dependency it pins:

- Round187 source SHA256:
  `6278b744f091657ff6035dc71a5656ba1ae861d3b672b591e6a77d718864c5cc`;
- Round190 source SHA256:
  `722e155df1ec992fc837603997151cda79e938b241c4761c5a958ee7665ad397`.

Round190 then rechecks the pinned Round180/Round184 formal chain.

The validated command was:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=193052 \
  /usr/bin/time -v \
  -o /tmp/cm2_round193_seed193052.time \
  .venv-neurips/bin/python \
  deliverables/cm2_round193_source_w_exact_near_positivity_probe.py \
  > /tmp/cm2_round193_seed193052.json \
  2> /tmp/cm2_round193_seed193052.stderr
```

It exited `0` in `5:14.53`, used `159,520 KiB` maximum RSS, and consumed
`314.24` user CPU seconds.  The script has no output-path option or
filesystem-write call; the shell and `/usr/bin/time` own the `/tmp`
captures.

The final JSON SHA256 is

`31e67957d433ba455aae4855ca6cb68a4dc090fb5b836fc3ca052ea7a96fd49d`.

Its canonical `probe_result` SHA256 is

`bd09c1ddb7e734bb32db8d0f9f9c203c74738a8f4d19f51c6c6bacaed2b8cc4f`.

## Exact input reconstruction

The probe rebuilt the exact corrected Round187 depth-2 residual:

- total residual cells: `37,262`;
- clipped target-first failures: `37,198`;
- full-p holdouts: `64`;
- original origins: `162`;
- residual key-set SHA256:
  `060ac08ec0ccb026ad4cf735a4ebe5af30753a690e7fbe80a4b95f25de3be19e`;
- exact total volume:
  `3297687/838860800000`.

The volume partition is

```text
3292023/838860800000
+ 177/26214400000
= 3297687/838860800000.
```

The 64 full-p cells occupy 8 origins, with origin-key SHA256

`2e0cc13c12e2117c893ba27c7e6c9f618ccde455153b4abf6e68b4eab33b53b7`.

They were not tested or credited by the exact-near path.

## Direct distance and identity cross-check

For every clipped cell, the preferred enclosure was rebuilt directly from
source and target geometry as

`dx^2 + dy^2 - R^2`.

The algebraically equivalent interval was independently evaluated as

`ell^2 - Delta`.

All `37,198/37,198` cells satisfy:

- direct distance margin: strictly positive;
- `ell^2 - Delta` interval: strictly positive;
- direct and identity interval enclosures overlap.

Thus interval dependency is not the obstacle.  Centered mean-value evaluation
and another outcome-blind coordinate split were correctly not triggered.

TAU and competitor checks also pass on every cell:

- `ell < TAU_MAX`: `37,198/37,198`;
- exactly one relevant competitor per cell;
- every competitor has an `earliest_lower`;
- every `competitor_lower - ell` margin is strictly positive.

The complete per-cell evidence-row SHA256 is

`5078b7a55df16967069bb6ea3ba721831fd1a85cab12fcf9eddebe6f77a72aa1`.

## Exact-near result

The exact-near route is invalidated by a strict sign, not by enclosure width:

- `ell` strictly positive: `0/37,198`;
- `ell` strictly negative: `37,198/37,198`;
- exact-near-positive cells: `0`;
- closed clipped cells: `0`;
- residual clipped cells: `37,198`;
- sole exact failure combination:
  `ELL_NOT_STRICT_POSITIVE`, count `37,198`;
- residual exact volume:
  `3292023/838860800000`;
- completely closed original origins: `0/162`.

The candidate-target distribution does not change this conclusion:

| candidate | cells |
|---|---:|
| `W[1,0]` | 28,976 |
| `G[0,0]` | 3,839 |
| `G[0,1]` | 3,839 |
| `W[3,-1]` | 232 |
| `W[3,1]` | 232 |
| `G[-2,0]` | 40 |
| `G[-2,1]` | 40 |

Every other replayed clipped-cell precondition passed; the only recorded
failure is `ell > 0`.

## The useful dual conclusion

Although the requested exact-near route fails, the same strict evidence gives
the opposite root classification on every cell.

For `Delta >= 0`,

```text
ell < 0
and ell^2 - Delta > 0
imply sqrt(Delta) < -ell
and therefore far = ell + sqrt(Delta) < 0.
```

Hence all `37,198` cells are classified diagnostically as
`EXACT_FAR_NEGATIVE`: both real roots, when present, lie strictly behind the
ray origin.  On `Delta < 0` the candidate has no real intersection.

This points to a different next proof: remove the candidate as a future-hit
competitor on all three Delta strata, then recompute the disposition of the
remaining target set.  It does not justify relabelling these cells as
exact-near-positive, and Round193 deliberately assigns this dual observation
zero closure and zero ledger credit.

The 64 full-p cells must remain separate until the same behind-target argument
or an explicit first-root-equality continuation is proved for them.

## Independent checks

A separate strict-JSON checker that did not import the Round193 script passed:

- canonical result-digest reconstruction;
- Round187 count and exact-volume partition;
- clipped closed/residual count and volume conservation;
- `37,198/37,198` direct/identity strict positivity and interval overlap;
- `0/37,198` exact-near and `37,198/37,198` diagnostic exact-far-negative;
- TAU and competitor-order census;
- full-p `64` cells / `8` origins holdout;
- whole-origin `0/162`; and
- all zero-promotion fields.

The stderr scan found no traceback, runtime error, assertion failure, or
failure marker.

## What worked

- The exact Round187 tail, key set, origin set, and rational volume were
  reproduced from pinned geometry.
- Direct distance and `ell^2 - Delta` gave two mutually overlapping,
  strictly positive enclosures on every cell.
- TAU and competitor order were independently replayed and passed globally.
- The experiment ruled out interval dependency as the blocker, avoiding
  unnecessary centered evaluation or another split.
- The strict negative sign of `ell` exposed a stronger, geometrically natural
  behind-target continuation.

## What failed

- The requested condition `ell > 0` fails strictly on every one of the
  37,198 cells.
- Exact-near positivity closes no clipped cell, split root, or original
  origin.
- The result cannot be rescued by centered arithmetic: the sign is strictly
  negative, not overwrapped.
- The 64 full-p cells remain outside this probe.

## Recommendation

Avoid further work on exact-near positivity for this tail.

The next bounded spike or formal route should implement
`EXACT_BEHIND_TARGET_REMOVAL`:

1. prove `ell < 0` and `distance^2-R^2 = ell^2-Delta > 0`;
2. conclude `far < 0` on the Delta-positive open side and the Delta-zero
   graph;
3. use no-real-intersection on the Delta-negative side;
4. remove the candidate on all three strata;
5. independently recompute the remaining-target disposition and complete
   the 3D/2D/1D/0D ledgers;
6. keep the 64 full-p cells in a separate exact-key table.

This Round193 spike issues strictly zero promotion:

- official-ledger mutations: `0`;
- whole-origin integer credits: `0`;
- Gate5: unchanged at `10/18`;
- complete 18-field blocks: unchanged at `0`;
- D02: `BLOCKED`;
- D03 negative oracle: `UNAUTHORIZED`;
- CM2: `NO-GO_FOR_CLAIM`.
