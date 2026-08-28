# CM2 Round183 — residual face-bracket refinement

Date: 2026-07-26  
Verdict: `PARTIAL_BOUNDED_FACE_BRACKET_RESIDUAL_REFINEMENT__NO_GLOBAL_DISPOSITION`

## Scope

Round183 pins the complete Round181 chain and performs a bounded,
dimension-safe refinement of all 3,812 Round181 residual parents.  The
dynamic pipeline receives 1,986 root inputs, 168 wall inputs, and 1,128
outgoing-chart inputs.  The remaining 530 collision1/source-seam carriers
are replayed unchanged in a separate ledger.

The refinement depths are:

- single-Delta and point-winner-nonstrict roots: 4;
- two-Delta roots: 6;
- wall pullbacks: 2;
- outgoing `H2` pullbacks: 4.

The contract is deliberately one-sided.  A nonzero derivative proves only
regularity if a graph exists.  A graph is certified nonempty only when a
strict opposite-sign boundary bracket is present.  The six original
two-Delta boxes are not promoted to Krawczyk incidences because no verified
rank-2 contraction and separate existence proof was obtained.

## Exact census

| Ledger | Boxes | Exact coordinate volume |
|---|---:|---:|
| Dynamic Round183 input | 3,282 | `338601/838860800000` |
| New local exact-key boxes | 17,376 | `6201903/26843545600000` |
| Dynamic residual terminals | 25,040 | `4633329/26843545600000` |
| Inherited collision1/source carriers | 530 | separately replayed |
| Combined residual | 25,570 | `697725681/26843545600000` |

The dynamic conservation identity is exact:

`6201903/26843545600000 + 4633329/26843545600000
= 338601/838860800000`.

The 17,376 local exact boxes split into 4,350 root, 4,594 wall, and
8,432 outgoing refinements.  Their four observed Gate5 ordinals are
290575, 291560, 321111, and 322097.  Every occurrence remains local:
global dispositions, whole-parent credit, and integer census delta are all
zero.

The 25,040 dynamic residual terminals are:

- 11,908 `OUTGOING_H2`;
- 8,214 `POINT_WINNER_NONSTRICT`;
- 4,800 `ACTIVE_DELTA_1`;
- 118 `ACTIVE_DELTA_2`.

## Dimension ledger

Round183 records 25,158 nominal 2D graph carriers:

- 13,250 candidate/incumbent carriers;
- 11,908 outgoing `H2` carriers;
- zero wall carriers after the bounded wall pipeline.

Of these, 8,468 have certified strict boundary brackets: 4,875 box-edge
brackets and 3,593 box-diagonal brackets.  The ledger retains 118 nominal
pairwise 1D incidence outers, zero certified unique 1D incidences, and zero
certified 0D multiple-incidence points.  Equality carriers are retained once
in their own dimension; no lower-dimensional carrier is subtracted as an
ambient 3D leaf.

## Independent verification

The verifier does not import or execute the Round183 producer.  It pins the
producer as inert source bytes, independently rebuilds the complete result
from Round181, and requires full canonical-result equality.

- certificate result digest:
  `f37eb4f1321ef837a2d67dbfaf7d3816dc320b81d31e151422eb9b649d5a5f53`;
- independently rebuilt result digest: identical;
- re-signed semantic attacks rejected: 28/28;
- strict JSON attacks rejected: 9/9;
- path/type attacks rejected: 11/11;
- producer and verifier seed-1/seed-987 cold replays: byte-identical;
- an additional parent cold replay at seed 183051 was also byte-identical.

## Nonpromotion and next gate

All 16 collision2 live strata remain partial.  Consequently:

- `D02 = BLOCKED`;
- Gate5 remains `10/18`;
- complete 18-field blocks remain `0`;
- `CM2 = NO-GO_FOR_CLAIM`.

The next residual round should preserve the four ledgers and attack them in
this order:

1. parametric interval-Newton contractions for the 11,908 outgoing `H2`
   tubes;
2. verified `C1`/rank contractions for 4,800 single-Delta and 118
   two-Delta tubes, with existence kept separate from rank;
3. owner/root face brackets for the 8,214 nonstrict tubes;
4. dimension-separated treatment of the 530 inherited collision1/source
   carriers.

No promotion is admissible unless every carrier required by a complete live
stratum closes under the same exact key.

