# CM2 Round270: OUTGOING-G factor-signature materialization

## Certified result

Round270 evaluates all `24,512` OUTGOING-G closed-leaf residuals from
Round269 with a target-specific exact geometry: fixed G center `(ix,iy)`,
radius `9/25`, and 256-bit Arb dual enclosures.

- `24,504` leaves are accepted;
- exact factor cells yield `37,712` complete ten-field side signatures;
- `8` leaves remain fail-closed at wall endpoint/count transitions;
- accepted leaves are disjoint from the frozen Round208 and Round269 leaf
  domains.

Certificate result SHA256:
`5c9c0585bf2cb664df493224f1005d4ef078d5e2f2e3044283019053b5e39add`.
Complete certificate SHA256:
`72a47e53ff601660cb63fe8062403e41a54450fa4a432638faf18a2c76b3efea`.

## Verification

The independent verifier pins the producer as inert bytes, rebuilds all
`24,512` decisions and `37,712` accepted signature rows, then requires exact
candidate-result equality.  It returns `PASS_INDEPENDENT_ROUND270`; all `5/5`
semantic attacks are rejected.  Seeds `270071` and `270929` produce identical
bytes.

## Strict non-promotion

Round270 awards zero expanded-occurrence, component-union, maximality, fibre,
global-disposition, or Jx/Jy glue credit.  The quotient remains `63,224`; the
expanded occurrence and exact-key frontiers remain `126,468 / 116`;
maximality remains `0/63,224`, fibres `0/116`, and dispositions
`0/224,580`.  Gate5 remains `10/18`, D02 remains blocked, and CM2 remains
`NO-GO_FOR_CLAIM`.

The closed-leaf residual is now `45,916`: `45,904` WALL leaves, `8`
OUTGOING-G wall-event leaves, and `4` OUTGOING-W derivative leaves.  Next:
close these twelve outgoing tails, materialize the WALL side arrangements,
then bind all signed regions and the frozen `152` true-seam patches to the
expanded component frontier.
