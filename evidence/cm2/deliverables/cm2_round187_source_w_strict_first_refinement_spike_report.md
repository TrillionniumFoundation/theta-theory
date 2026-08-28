# CM2 Round187 — source-W strict-first refinement spike

Date: 2026-07-26  
Verdict: `PARTIAL`

## Question

Can a bounded two-level refinement of the 16,492
`TARGET_NOT_STRICT_POSITIVE_FIRST` cells in the Round184 pure clipped-Delta
tranche completely close any of the 162 affected source-W original origins,
while preserving exact dimension/volume accounting, holding all source seams
apart, and issuing no official-ledger or global promotion?

## Method

The read-only probe
`cm2_round187_source_w_strict_first_refinement_probe.py` was frozen at SHA256

`6278b744f091657ff6035dc71a5656ba1ae861d3b672b591e6a77d718864c5cc`.

It pins the Round180 and Round184 inputs, treats the Round184 producer as inert
bytes, and rebuilds the relevant Round184 children from the pinned independent
Round180/Round176 geometry.  It independently reconfirms the exact cohort:

- `162` affected original origins;
- `18,084` Round184 residual children;
- `1,592` children already closed by the Round184 clipped-Delta proof; and
- `16,492` cells failing specifically at
  `TARGET_NOT_STRICT_POSITIVE_FIRST`.

For each failed cell, the probe applies at most two additional deterministic
binary splits.  Every evaluated child first passes through the pinned
Round180/Round176 direct strict terminal path.  A child is counted closed only
when the whole closed box has coarse disposition `EXCLUDED` and all owned
boundary strata inherit that strict proof.  Direct `LIVE` or `MIXED` outcomes
would remain residual.  Only a child without a direct terminal disposition is
then tested by the Round184-equivalent clipped-Delta three-stratum proof.

The validated command was:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=187052 \
  /usr/bin/time -v \
  -o /tmp/cm2_round187_depth2.time \
  .venv-neurips/bin/python \
  deliverables/cm2_round187_source_w_strict_first_refinement_probe.py \
  --extra-depth 2 \
  > /tmp/cm2_round187_depth2.json \
  2> /tmp/cm2_round187_depth2.stderr
```

The probe has no output-path option, performs no delivery or ledger writes,
prints progress only on stderr, and emits one final JSON document on stdout.

An initial run exposed a probe-criterion defect: refined children with zero
unresolved discriminant targets were being retained wholesale instead of
first receiving the direct strict terminal test.  That initial result was
discarded.  The direct-strict-first branch was added, the script was
recompiled and statically rechecked for read-only behavior, and the complete
depth-2 run was repeated.  All statistics below are from that final corrected
run only.

## Evidence

The corrected run exited `0` and produced result SHA256

`1bdeeefc90c850af0370453d0cce039141a6a64c3ac3e6d4a8c0a145f40226c0`.

Resource use was:

- elapsed wall time: `4:30.74`;
- maximum RSS: `137,608 KiB`;
- evaluated nodes: `99,828`;
- split parents: `41,668`;
- split-axis census: `p=16,492`, `t=25,176`.

The exact Round184 cohort volume was

`800217/104857600000`.

It decomposes before the new refinement as:

- Round184-closed child volume:
  `35223/52428800000`;
- strict-first failure-cell input volume:
  `729771/104857600000`.

The depth-2 refinement of those 16,492 failure roots produced:

- `20,898` closed terminal cells, all by
  `DIRECT_STRICT_CLOSED_BOX` with coarse disposition `EXCLUDED`;
- closed refined volume:
  `2540481/838860800000`;
- `37,262` residual terminal cells;
- residual volume:
  `3297687/838860800000`.

Thus the corrected refinement closes exactly `43.515038%` of the input
failure-cell volume and retains `56.484962%`.  Including the 1,592
Round184-closed children, the total closed support volume is

`3104049/838860800000`,

and exact conservation is

`3104049/838860800000 + 3297687/838860800000`

`= 800217/104857600000`.

The residual terminal taxonomy is:

- `37,198` cells:
  `TARGET_NOT_STRICT_POSITIVE_FIRST`;
- `64` cells:
  `NOT_CLIPPED_FULL_P_GRAPH`.

The binary-forest identities were independently rechecked:

- `99,828 = 16,492 + 2*41,668` evaluated nodes;
- `58,160 = 20,898 + 37,262 = 16,492 + 41,668` terminal leaves.

The canonical result hash, strict JSON parse, exact cohort census, binary-tree
accounting, rational volume identities, source-seam partition, stderr error
scan, and zero-promotion fields all passed.

All `162` affected origins retain at least one residual terminal cell:

- newly completely closed original origins: `0`;
- residual original origins: `162`.

All `18` Round184 pure-tranche physical source-seam origins remain a separate
holdout:

- `6` lie inside the 162-origin strict-first cohort;
- `12` lie outside that cohort;
- source-seam half-open owner: `E`;
- probe source-seam official credit: `0`.

## What worked

- The Round184 cohort and all 18,084 residual children were reproduced from
  pinned independent geometry rather than trusted as probe-generated rows.
- The corrected direct strict terminal path closed 20,898 refined cells with
  whole-box `EXCLUDED` proofs and owned-boundary inheritance.
- Exact rational volume conservation held at the failure-cell level and over
  the complete Round184 residual support.
- The refinement removed `43.515038%` of the strict-first failure volume at
  depth two.
- The 18 source seams stayed dimension-safe and separate from physical-parent
  credit.
- The final run was deterministic under the fixed hash seed and passed all
  document, census, tree, volume, and zero-promotion checks.

## What failed

- No affected original origin was completely closed: the whole-origin gain is
  `0/162`.
- `37,198` terminal cells still fail the strict-positive-first condition.
- `64` terminals moved into the full-p discriminant-graph regime, which is
  outside the clipped-Delta proof contract and belongs with a root-equality
  continuation.
- Every one of the 20,898 new cell closures came from the direct strict
  terminal branch.  The clipped-Delta three-stratum branch produced no new
  terminal closure after refinement.
- Therefore cell-volume decay does not yet translate into official
  whole-origin closure.

## Recommendation

Do not launch a blind full depth-4 continuation as the next core action.
Depth two removed substantial volume but closed no whole origin, so two more
levels under the unchanged longest-width rule have poor expected return for
the official whole-origin metric.

First strengthen the continuation in two targeted ways:

1. attack the remaining strict-first gap directly with a centered first-time
   separation bound and a split-axis rule driven by the weakest root-order
   margin rather than coordinate width alone;
2. move the 64 full-p graph cells into an explicit first-root-equality proof
   instead of treating them as clipped-Delta residuals.

A later depth-4 run may be useful as a bounded decay diagnostic after those
two changes, but it should not be treated as a promotion route by itself.

This spike issues strictly zero promotion:

- official-ledger mutations: `0`;
- whole-origin integer credits issued: `0`;
- probe counts applied to the official ledger: `false`;
- source-seam credit: `0`;
- global Gate5: unchanged at `10/18`;
- complete global 18-field blocks: unchanged at `0`;
- D02: `BLOCKED`;
- D03 negative oracle: `UNAUTHORIZED`;
- CM2: `NO-GO_FOR_CLAIM`.

