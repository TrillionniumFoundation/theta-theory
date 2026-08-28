# CM2 Round200 — collision-two stable-root spike

Date: 2026-07-26  
Verdict: `INVALIDATED` as a whole-box closure route

## Question

Can the 9,076 Round185 `POINT_WINNER_NONSTRICT` dynamic residual boxes be
closed merely by replacing the cancellation-prone near-root expression

`ell - sqrt(Delta)`

with the algebraically identical stable expression

`(distance^2 - radius^2) / (ell + sqrt(Delta))`?

This is a read-only feasibility probe.  It pins and checks the complete
six-file Round185 formal package, rebuilds every candidate on every input
box at 384-bit Arb precision, writes no artifact, and awards no formal or
global credit.

## Result

The stable expression is useful, but it is not the missing whole-box gate.

- input boxes: `9,076`
- input origins: `4`
- exact input coordinate volume: `54339/1342177280000`
- input incumbent roots newly proved strict future by stable
  rationalization: `4,370`
- input incumbent roots still crossing `Delta=0`: `4,706`
- total stable-rationalized strict-future candidate occurrences: `5,264`
- centered-C0 candidate exclusions added: `448`
- remaining unresolved `Delta=0` occurrences: `11,928`
- locally exact 3D rows produced: `0`
- residual boxes: `9,076`

Every box still contains at least one unresolved candidate birth surface.
Consequently stable owner selection remains
`UNRESOLVED_CANDIDATE_ROOTS` on all `9,076` boxes.  The unresolved
occurrences are:

- `G[1,0]`: `2,728`
- `G[1,1]`: `2,728`
- `W[1,-1]`: `3,236`
- `W[1,1]`: `3,236`

The exact-volume conservation check is

`54339/1342177280000 = 54339/1342177280000 residual + 0 exact`.

## Why the attempted closure fails

When centered C0 proves `Delta>0`, the stable formula removes interval
subtraction loss and rigorously proves a positive near root whenever
`ell>0` and `distance^2-radius^2>0`.  The probe also requires the raw and
stable root enclosures to overlap.

But a candidate whose `Delta` changes sign is genuinely absent on one side
of a two-dimensional birth surface and present on the other.  A stable root
formula cannot erase that surface.  Treating it as a whole-box owner would
conflate numerical regularization with geometric existence.

## Next bounded gate

The next valid route is a dimension-safe `Delta=0` arrangement over the
four affected origins:

1. isolate each of the 11,928 birth surfaces with a strict graph axis;
2. use the stable root only on the `Delta>0` side;
3. order the newborn root against the incumbent on each open side;
4. retain the `Delta=0` sheet, its boundary curves, and endpoints in
   separate 2D/1D/0D ledgers;
5. materialize a local exact key only after the selected owner, wall word,
   outgoing chart, and all lower-dimensional glue agree.

No further blind root refinement is justified by this spike.

## Reproducibility

- probe:
  `cm2_round200_collision2_stable_root_probe.py`
- probe SHA256:
  `7bfa5664636964299a56fb06da3c127b1fb8591fd2f289e271496668f4dbc11d`
- seed:
  `PYTHONHASHSEED=200052`
- output SHA256:
  `86cdc5b5e0c45205d764a0ac55127f76e94ebd0ebbf3eb50ffbf827a59194c57`
- result SHA256:
  `4682d7cd06747329ff4f1753e7f77143e90ccd28fafd5fc8b24bda80fff18172`
- elapsed:
  `1:42.44`
- maximum RSS:
  `605,928 KiB`

AST parsing and canonical result rehash passed.  The script has no output
path and performs no filesystem mutation.

## Strict state

This negative spike changes no formal ledger:

- `D02 = BLOCKED`
- Gate5 remains `10/18`
- complete 18-field blocks remain `0`
- `CM2 = NO-GO_FOR_CLAIM`

