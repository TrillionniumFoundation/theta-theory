# CM2 Round306 C51 pair-1 dual-task route probe v1

Status: **PASS TWO COMPLETE DUAL-SIDE STRICT ROUTE FRONTIERS; PENDING GLOBAL
OWNER, INDEPENDENT VERIFIER, AND SEAL; ZERO FORMAL/D02 CREDIT**.

## Frozen scope

- C46 64-shard plan object:
  `7d004f59282dee21a28db0cd0b727a9045f4befce207c96be4efb07d1399c9bf`
- Probe source SHA-256:
  `caf043d2a475f8c25e92785587db971a0d33242b8560dd096f09a1e5c6e72069`
- Full cold probe object SHA-256:
  `187344a3c524dce1898151bf64f507c181dde137a3710eb9bc5cd1b895a81f6e`
- Event budget supplied: 16.  It was a resource ceiling only; the computation
  stopped after mathematical closure at one and six splits respectively.

The exact pair-1 direct queue contains two C2 wall-endpoint tasks:

```text
daada4d9fd48677629cbfa9872b073d5fdf1552b115bf94438e7357f9a5dd95b
e37b527423ad1aabba7485faacd03f7bb95ba9d79caebd614fb63d38ccd8dac6
```

## Exact route result

The first task required one exact `t` split and closed on both physical sides
at relative frontier:

```text
0, 1
```

Both leaves independently reproduce strict collision-two owner mismatch,
complete 55-candidate/root-order margins, representative owner `G[1,0]`, and
reflected owner `G[1,1]`.  The frontier is prefix-free with Kraft sum one.

The second task required six exact adaptive splits.  Its final dual-side
strict frontier is:

```text
00, 01, 10, 110, 1110, 11110, 11111
```

The apparently terminal C39 W-side rows were not accepted from their labels.
For each, the probe reran the exact dynamic collision-two classifier and the
complete strict margin reconstruction.  Intermediate paths `1`, `11`, `111`,
and `1111` remained exact `WALL_ENDPOINT` states and were split; the final
seven leaves all close independently on both physical sides.  This frontier
is also prefix-free with exact Kraft sum one.

Across the two tasks, the final result contains nine logical leaves and 18
physical-side strict terminal rows.  No fixed-depth inference or limiting
endpoint claim was used.

## Strict boundary

This is producer-import route feasibility evidence, not a D02-A candidate or
authority.  It has not yet:

- rebuilt the full active occurrence overlay for both replacements;
- atomized and assigned all global face/endpoint/corner owners;
- run a no-producer-import independent numerical verifier;
- created a pair-level successor, receipt, pointer, or no-replace seal;
- updated the 862-parent conservation or 76,832 census.

Therefore the formal coarse authority remains exactly `574 paired / 1,150
unresolved / 575 representatives remaining`.  The planned `576 / 1,148 / 574`
transition is unauthorized until every remaining obligation above passes.

## Replay

```bash
.cm2-runtime/python-flint-0.9.0/bin/python -I -B \
  deliverables/cm2_round306c51_d02a_pair1_two_task_route_probe_v1.py \
  --probe --event-budget 16
```
