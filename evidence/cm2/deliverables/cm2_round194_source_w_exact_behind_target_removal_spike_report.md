# CM2 Round194 — source-W exact-behind candidate-removal spike

Date: 2026-07-26  
Verdict: `VALIDATED`

## Question

Can the exact-behind rule close the complete Round187 depth-2 residual,
including both 37,198 clipped cells and all 64 full-p holdouts, without
requiring a discriminant graph to exist?

For each whole closed box the rule is:

```text
ell < 0
and distance^2 - R^2 = ell^2 - Delta > 0.
```

If `Delta < 0`, the candidate has no real root.  If `Delta >= 0`, these
inequalities imply

`far = ell + sqrt(Delta) < 0`.

The candidate therefore has no future root anywhere on the box.  It can be
deleted before independently rebuilding the remaining-record leaf, owner,
outgoing chart, and terminal disposition.

## Frozen probe and command

The read-only probe
`cm2_round194_source_w_exact_behind_target_removal_probe.py` is frozen at
SHA256

`d4eb7ba9f2932083da2266a0ae67df7b4b941625472849fb9a52cbdc8e7c371f`.

It pins, before import:

- Round187 source:
  `6278b744f091657ff6035dc71a5656ba1ae861d3b672b591e6a77d718864c5cc`;
- Round190 source:
  `722e155df1ec992fc837603997151cda79e938b241c4761c5a958ee7665ad397`;
- Round193 source:
  `fca55b9f9a28aeda65f2e4a5a2305e704f198b3f08d10891fe607f46273f3a52`.

The validated full command was:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=194052 \
  /usr/bin/time -v \
  -o /tmp/cm2_round194_seed194052.time \
  .venv-neurips/bin/python \
  deliverables/cm2_round194_source_w_exact_behind_target_removal_probe.py \
  > /tmp/cm2_round194_seed194052.json \
  2> /tmp/cm2_round194_seed194052.stderr
```

It exited `0` in `5:02.71`, used `160,120 KiB` maximum RSS, and consumed
`302.35` user CPU seconds.  The script has no output-path option or
filesystem-write call; the shell and `/usr/bin/time` own the `/tmp`
captures.

The final JSON SHA256 is

`47e698cb15affd252f59ae02976654e37f8c5eb9d6afca7c48f50672b83b71e9`.

Its canonical `probe_result` SHA256 is

`0e3c0422d69ca9aa782a717898e34be752e8623de515f3ca61ab89a2cbc0c55e`.

## Exact input

The exact Round187 depth-2 residual was reconstructed from pinned geometry:

| input class | cells | exact volume |
|---|---:|---:|
| target-first clipped | 37,198 | `3292023/838860800000` |
| full-p holdout | 64 | `177/26214400000` |
| total | 37,262 | `3297687/838860800000` |

The 162-origin key digest is

`c86ec3a7042b6aaa58eee59ec43a6ec2ebda8bd192cedfcf4c47d8c42c4615c3`,

and the 37,262-cell key digest is

`060ac08ec0ccb026ad4cf735a4ebe5af30753a690e7fbe80a4b95f25de3be19e`.

## Exact-behind evidence

All `37,262/37,262` cells satisfy:

- `ell`: strictly negative;
- direct `distance^2-R^2`: strictly positive;
- independent `ell^2-Delta` enclosure: strictly positive;
- direct and identity enclosures overlap;
- exact-behind contract: pass.

Every candidate `Delta` enclosure overwraps zero.  This does not block the
proof because the two Delta signs are covered logically; no graph existence,
nonemptiness, bracket, or topology is needed.

The candidate-target census is:

| candidate | all cells | of which full-p |
|---|---:|---:|
| `W[1,0]` | 29,008 | 32 |
| `G[0,0]` | 3,839 | 0 |
| `G[0,1]` | 3,839 | 0 |
| `W[3,-1]` | 240 | 8 |
| `W[3,1]` | 240 | 8 |
| `G[-2,0]` | 48 | 8 |
| `G[-2,1]` | 48 | 8 |

The full per-cell evidence digest is

`7318ae19f7f0ef239f17c9a461ffbe244cfddb5a2f2994dc98154ff368005d31`.

## Independent reduced-record classification

After deleting the exact-behind candidate, every cell was rebuilt from its
remaining records rather than inheriting the pre-deletion label:

- remaining records per cell: exactly `1`;
- remaining record class: `strict_future_root`, `37,262`;
- remaining leaf class: `unique_first`, `37,262`;
- remaining active-target count: exactly `1`;
- reduced terminal dispositions:
  - `EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH`: `31,534`;
  - `EXCLUDED_OUTGOING_CHART_MISMATCH`: `5,728`;
- unresolved or live reduced disposition: `0`.

The 5,728 frozen-owner cases independently recompute outgoing chart as:

- `N`: `2,864`;
- `S`: `2,864`;

both mismatching the frozen `W` chart.  The remaining 31,534 cells have an
owner different from the frozen owner, so outgoing-chart recomputation is not
applicable.

Thus:

- clipped cells closed: `37,198/37,198`;
- full-p cells closed: `64/64`;
- all cells closed: `37,262/37,262`;
- closed exact volume: `3297687/838860800000`;
- residual cells and volume: `0`;
- closed-cell key digest equals the complete input-cell key digest.

All classwise and global count and exact-volume conservation identities pass.

## Whole origins and source strata

The probe geometrically closes the residual support of all `162/162`
affected origins:

- strict physical interior: `156`;
- physical source-seam composite: `6`;
- residual origins: `0`.

The strict-interior origin digest is

`801ea4127662806c9e29f8d356ad09279e528460109d71f929ba5ebe51b0f7fd`.

The six source-seam keys retain their separate half-open source-domain
requirement and have digest

`d21a934ed6d43ba876ab514cd710b0f659f3e94e543b3c4e11ea6d719fe0d208`.

They receive no origin credit in this probe.

The 64 full-p cells belong to 8 origins:

- all 8 are strict physical interior;
- full-p/source-seam overlap: `0`;
- full-p origin-key digest:
  `2e0cc13c12e2117c893ba27c7e6c9f618ccde455153b4abf6e68b4eab33b53b7`.

## Generality

All 64 full-p cells pass the same proof as the clipped cells.  Since the rule
does not inspect whether a Delta graph is clipped, full, empty, or nonempty,
the exact-behind reduction is eligible for a bounded scan of the mixed and
root-equality priority registry.

This is a rule-level generalization, not a claim that every future registry
cell will pass.  Each cell must independently establish:

1. `ell < 0`;
2. `distance^2-R^2 > 0`;
3. direct/identity consistency; and
4. an excluded reduced-record disposition after deletion.

Compact-q, grazing/source strata, multiple simultaneous candidates, and
physical source seams remain separately typed and cannot inherit credit merely
because one candidate was deleted.

## Independent checks

A separate strict-JSON checker that did not import the Round194 probe passed:

- canonical result-digest reconstruction;
- input-class count and exact-volume partition;
- exact-behind `37,262/37,262`;
- excluded reduced disposition `37,262/37,262`;
- per-class and global closed/residual conservation;
- all 64 full-p cells and their 8 strict-interior origins;
- origin partition `162 = 156 strict interior + 6 source seam`;
- graph-topology nondependence; and
- all zero-promotion fields.

The stderr scan found no traceback, runtime error, assertion failure, or
failure marker.

## What worked

- One graph-topology-independent rule handled clipped and full-p cells
  uniformly.
- Exact negative ell and positive distance margin were strict on every cell.
- Candidate deletion was followed by an independent remaining-record rebuild.
- Every reduced cell obtained a strict excluded disposition.
- The complete input key set and exact volume closed with zero residual.
- Full-p success validates scanning mixed/root-equality registry rows next.

## What remains

- This is a read-only probe, not a formal certificate.
- The six physical source-seam origins still need their half-open source
  partition.
- Complete 3D/2D/1D/0D ledgers, lineage rows, attacks, independent verifier,
  cold replay, and manifest do not yet exist.
- Compact-q and other source-stratum contracts remain independent.
- No official source-W or global integer ledger has changed.

## Recommendation

Proceed in two bounded tracks:

1. formalize exact-behind candidate removal for this 37,262-cell cohort with
   complete per-cell evidence and an independent non-importing verifier;
2. scan the outcome-blind frozen mixed/root-equality registry for the same
   per-candidate deletion rule, while preserving compact-q, grazing, and
   source-seam partitions.

This spike issues strictly zero promotion:

- official-ledger mutations: `0`;
- whole-origin integer credits: `0`;
- Gate5: unchanged at `10/18`;
- complete 18-field blocks: unchanged at `0`;
- D02: `BLOCKED`;
- D03 negative oracle: `UNAUTHORIZED`;
- CM2: `NO-GO_FOR_CLAIM`.
