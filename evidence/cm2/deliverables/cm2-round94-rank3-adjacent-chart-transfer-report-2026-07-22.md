# CM2 Round 94 — adjacent-chart transfer and physical terminal events

Date: 2026-07-22 (Asia/Shanghai)

## Result

All 28 Round93 dominant-coordinate chart seams transfer to exactly one adjacent
source chart.  The transfer census is:

```text
E->N 3   E->S 3   N->E 4   N->W 3
S->E 3   S->W 3   W->N 5   W->S 4
```

Every transferred algebraic branch remains inside that adjacent chart until
source grazing; no branch encounters a second chart seam.

The physical next-tangency status has a sharper terminal census:

```text
physical next tangency until source grazing:                25
occluded first by an earlier third-collision owner:           3
```

The three finite occlusion rows are:

| Source core | Designated third target | Adjacent chart | Earlier owner |
|---:|---|---|---|
| 12 | `G[3,-1]` | `S` | `W[1,-1]` |
| 13 | `G[3,2]`  | `N` | `W[1,1]`  |
| 16 | `G[2,3]`  | `E` | `W[1,1]`  |

Each physical prefix carries 64 strict point replays, for 1,792/1,792
transferred point states.  Together with the 37 direct-grazing Round93 rays,
the 65 exterior rays now have a finite physical terminal-event census:
62 source-grazing terminals and three earlier-owner occlusion terminals.

## Strict boundary

The intervals between strict probes are not yet covered by a common centered
source-coordinate Taylor model.  Therefore this is a finite terminal-event
frontier, not yet a complete physical-face quotient.  No RN row or Gate-5
field is installed.

## Verification

- producer precision: 512 bits;
- independent replay precision: 640 bits;
- unique seam transfers: 28/28;
- transferred physical-prefix probes: 1,792/1,792;
- semantic mutations rejected: 3/3;
- strict JSON, Python compile, and SHA checks: pass.

## Next route

Construct one centered Taylor enclosure of the reverse source-coordinate map
on each finite probe gap.  The 62 grazing and three occlusion brackets then
provide the true endpoint registry for rebuilding the rank-three face quotient.

