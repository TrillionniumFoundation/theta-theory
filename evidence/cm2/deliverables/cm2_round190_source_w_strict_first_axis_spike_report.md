# CM2 Round190 — source-W strict-first fixed-axis diagnostic spike

Date: 2026-07-26  
Verdict: `PARTIAL`

## Question

For the exact Round187 depth-2 source-W residual, which primitive condition
causes all remaining `TARGET_NOT_STRICT_POSITIVE_FIRST` failures, and does one
additional globally fixed `t`, `p`, or `s` split close any whole original
origin?  The comparison must use identical inputs and issue zero official
credit.

## Frozen probe and command

The read-only probe
`cm2_round190_source_w_strict_first_axis_probe.py` is frozen at SHA256

`722e155df1ec992fc837603997151cda79e938b241c4761c5a958ee7665ad397`.

It pins the complete Round180 and Round184 deliveries before importing the
final Round187 probe, whose required source SHA256 is

`6278b744f091657ff6035dc71a5656ba1ae861d3b672b591e6a77d718864c5cc`.

The Round184 six-item manifest SHA256 is

`3c2a50663dc47479f67435109b737362895e53a2c1b4c29991fe875c5ac68cd1`,

and the pinned formal Round184 verification result is

`126bf98cd4bdc1fc7a69b2a57329b89359b74749bbbd1f43fdbccbc816add9e9`.

The validated full command was:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=190052 \
  /usr/bin/time -v \
  -o /tmp/cm2_round190_seed190052.time \
  .venv-neurips/bin/python \
  deliverables/cm2_round190_source_w_strict_first_axis_probe.py \
  > /tmp/cm2_round190_seed190052.json \
  2> /tmp/cm2_round190_seed190052.stderr
```

The run exited `0` in `6:59.01`, used `299,124 KiB` maximum RSS, and
consumed `418.48` user CPU seconds.  The script itself has no output-path
option or filesystem-write call; the shell and `/usr/bin/time` own the three
`/tmp` captures.

The final JSON file SHA256 is

`a76cc318808ac66061d0f023594cd8043fb563b0ee20eeb1976a70adbbf763e9`.

Its canonical `probe_result` SHA256 is

`c53a6894e325f59a7dada6f3d84dbd90d22ce5061c4a149d71b429762e66b7a9`.

## Exact Round187 reconstruction

The probe independently rebuilt the corrected Round187 depth-2 forest rather
than trusting aggregate values from its prior JSON:

- residual cells: `37,262`;
- `TARGET_NOT_STRICT_POSITIVE_FIRST`: `37,198`;
- `NOT_CLIPPED_FULL_P_GRAPH`: `64`;
- affected original origins: `162`;
- residual key-set SHA256:
  `060ac08ec0ccb026ad4cf735a4ebe5af30753a690e7fbe80a4b95f25de3be19e`;
- exact total residual volume:
  `3297687/838860800000`.

The exact volume partition is

```text
3292023/838860800000
+ 177/26214400000
= 3297687/838860800000,
```

where the first term is the 37,198 target-order cells and the second is the
64 full-p holdouts.

## Failure-mask census

The original `target_positive_first` predicate was reconstructed as four
individually checkable conditions:

1. `candidate.ell - target_radius > 0`;
2. `candidate.ell < TAU_MAX`;
3. every relevant competitor has an `earliest_lower`;
4. `candidate.ell < competitor.earliest_lower` for every such competitor.

The census is unexpectedly clean:

- all `37,198/37,198` cells fail exclusively at condition 1,
  `ELL_MINUS_RADIUS_NOT_STRICT_POSITIVE`;
- overlap failures: `0`;
- `TAU_MAX - ell` is strictly positive on all `37,198` cells;
- every cell has exactly one relevant competitor;
- every competitor has an `earliest_lower`;
- every competitor lower-minus-target-ell margin is strictly positive;
- failing competitor counts: `0` on all cells;
- `ell - radius` is strictly negative, not merely interval-overwrapped, on
  every cell.

The failure-mask row digest is

`6be17d4fcbe1ab7267ce855008e47d91724fb8b6a5aac9937475660681afc091`.

Candidate obstacles are `W: 29,440` and `G: 7,758`.  The candidate-target
census is:

| target | cells |
|---|---:|
| `W[1,0]` | 28,976 |
| `G[0,0]` | 3,839 |
| `G[0,1]` | 3,839 |
| `W[3,-1]` | 232 |
| `W[3,1]` | 232 |
| `G[-2,0]` | 40 |
| `G[-2,1]` | 40 |

Thus competitor ordering and the time horizon are not the active breakpoints.
The sole breakpoint is the deliberately coarse radius-wide sufficient bound
used for target-root positivity.

## Equal-input fixed-axis comparison

Each axis sees the same 37,198 roots and exact input volume
`3292023/838860800000`.  Each child is tested in this fixed order:

1. direct strict terminal;
2. direct `EXCLUDED` closes the whole child;
3. direct `LIVE` or `MIXED` remains residual;
4. otherwise apply the Round184-equivalent clipped-Delta three-stratum proof.

All new closures came from `DIRECT_STRICT_CLOSED_BOX`; the clipped-Delta branch
added zero new closures.

| fixed axis | closed children / 74,396 | closed volume | fully closed split roots / 37,198 | residual reasons | whole origins closed |
|---|---:|---:|---:|---|---:|
| `t` | 13,328 (17.914942%) | `147441/209715200000` | 1,844 (4.957256%) | target `55,884`; new full-p `5,184` | 0 |
| `p` | 17,430 (23.428679%) | `308511/335544320000` | 672 (1.806549%) | target `56,966`; new full-p `0` | 0 |
| `s` | 7,394 (9.938706%) | `654369/1677721600000` | 3,152 (8.473574%) | target `66,106`; new full-p `896` | 0 |

For every axis, closed plus residual child counts equal `74,396`, closed plus
residual exact volume equals the common input volume, the three root-status
counts equal `37,198`, and residual-reason volumes equal residual volume.
All `162` original origins remain residual under every globally fixed axis.

There is no universally dominant axis:

- `s` is recommended under the whole-origin-oriented lexicographic objective:
  whole origins first (all tied at zero), then fully closed split roots.  It
  closes `3,152`, versus `1,844` for `t` and `672` for `p`.
- `p` is best if the objective is closed child count or exact excluded
  volume, and it is the only axis that creates no new full-p regime.

Consequently, the `s` recommendation is conditional on split-root closure
being the next proxy for eventual whole-origin credit; it is not a claim that
`s` dominates `p` in volume or regime stability.

## Post-hoc best-per-cell boundary

As a diagnostic upper comparison only, the probe also chooses the axis after
observing all three child outcomes for each parent.  With deterministic
`t,p,s` tie order it yields:

- closed children: `20,474`;
- fully closed split roots: `3,716`;
- closed volume: `1811949/1677721600000`;
- residual children: `53,922`;
- residual reasons: target `48,754`, full-p `5,168`;
- whole original origins closed: `0`.

Its outcome-row SHA256 is

`58f4f197658e187bd8fd59296985f4973b06aed9cadb84409f8a7f6f05db66e9`.

This selector is not outcome-blind: it reads the very closure outcomes it is
trying to optimize.  Therefore none of its counts can be used by a formal
certificate, even if copied into a producer and re-signed.  A future
per-cell selector must be frozen from parent-only evidence before any child
proof is evaluated, and then independently replayed.

The fixed-axis rows have a narrower status.  They are valid equal-input A/B
probe evidence because each axis is globally fixed before child evaluation,
but they still issue no official ledger credit.  Promotion would require a
formal producer, an independent verifier that does not import the producer,
complete per-cell evidence, attacks, cold replay, and a manifest.

## Independent checks

A separate strict-JSON checker, which did not import the Round190 script,
recomputed and passed:

- canonical result digest;
- Round187 count and exact-volume partition;
- exclusive/overlap failure-mask partition;
- each fixed axis's child, root, exact-volume, and residual-reason
  conservation;
- post-hoc count, exact-volume, and residual-reason conservation;
- all `0/162` whole-origin outcomes; and
- the zero-promotion fields.

The stderr error scan found no traceback, runtime error, assertion failure, or
failure marker.

## What worked

- The exact Round187 residual, key digest, origin set, and rational volume were
  rebuilt from pinned geometry.
- The failure-mask census isolated one primitive breakpoint without overlap:
  the radius-wide target-root positivity bound.
- All three fixed axes were compared on identical cells with exact
  conservation.
- The experiment quantified the root-closure versus volume-closure tradeoff.
- The post-hoc selector was explicitly separated from certificate-admissible
  selection.

## What failed

- No fixed axis closes any whole original origin: `0/162`.
- No refined child is newly closed by the clipped-Delta proof itself.
- Coordinate bisection only transfers some cells to direct strict exclusions;
  it does not repair the coarse target-positive-first argument.
- `t` and `s` create additional full-p residuals, while `p` closes few complete
  split roots.
- The post-hoc upper comparison also closes `0/162` origins and is
  outcome-dependent.

## Recommendation

Do not formalize another blind coordinate-depth continuation.

The next mathematical criterion should replace the coarse
`ell - radius > 0` sufficient condition with a clipped-stratum-aware target
near-root bound, for example a centered enclosure of

`ell - sqrt(max(Delta, 0)) > 0`

on the Delta-positive side, with its graph and boundary limits handled
dimension-safely.  If a per-cell split is still required, freeze an
outcome-blind selector using only parent failure masks and the predicted
interval-width contraction of that near-root margin; use a fixed `t,p,s`
tie rule and evaluate child proofs only afterward.

Keep the original 64 full-p cells, plus any full-p cells created by a chosen
axis, in a separate explicit first-root-equality continuation.

This spike issues strictly zero promotion:

- official-ledger mutations: `0`;
- whole-origin integer credits: `0`;
- post-hoc credits: `0`;
- Gate5: unchanged at `10/18`;
- complete 18-field blocks: unchanged at `0`;
- D02: `BLOCKED`;
- D03 negative oracle: `UNAUTHORIZED`;
- CM2: `NO-GO_FOR_CLAIM`.
