# CM2 Round269: closed-collar direct side-signature materialization

## Certified result

Round269 evaluates all `184,452` positive-volume closed Round182 collar leaves
with the pinned Round195/Round198/Round207 exact evaluator chain at fixed
256-bit Arb precision.

- `114,032` closed OUTGOING-W leaves are accepted;
- their exact factor decomposition yields `187,128` complete ten-field local
  return side signatures;
- the accepted leaves are disjoint from the `18,324` residual leaves carrying
  the `36,040` already frozen Round208 formal rows;
- `70,420` leaves remain explicit fail-closed residuals.

The residual census is exact: `45,904` WALL leaves, `24,512` OUTGOING-G
leaves outside the pinned W-target evaluator domain, and `4` OUTGOING-W
leaves whose whole-leaf strict t-derivative proof does not close.

Certificate result SHA256:
`2e8071d2a99a206177f5293747bc7c7c9b1716184f4084c4f22fd3cf5bf45b7d`.
Complete certificate SHA256:
`472df3ac65c490b79924beaabb382435f5b74ea8ac6c13d71b1d0ab54ffe01d3`.

## Verification

The verifier pins the producer as inert bytes and independently recomputes
all `184,452` decisions and `187,128` accepted rows before opening the
305 MiB candidate.  It requires exact result-object equality and returns
`PASS_INDEPENDENT_ROUND269`; all `5/5` semantic attacks are rejected.  Seeds
`269071` and `269929` produce identical result and certificate bytes.

## Strict non-promotion

These are local side signatures, not expanded occurrences.  Round269 awards
zero occurrence, component-union, maximality, fibre, global-disposition, or
Jx/Jy glue credit.  The frozen quotient remains `63,224`; the expanded
occurrence and exact-key frontiers remain `126,468 / 116`; maximality remains
`0/63,224`, fibres `0/116`, and dispositions `0/224,580`.  Gate5 remains
`10/18`, D02 remains blocked, and CM2 remains `NO-GO_FOR_CLAIM`.

Next: build a separately pinned OUTGOING-G factor-cell evaluator for `24,512`
leaves, close the four OUTGOING-W derivative residuals, materialize the
`45,904` WALL leaves by exact side-specific integer-wall insertion, and then
bind all signed regions plus the frozen `152` true-seam patches to the
expanded component frontier.
