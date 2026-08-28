# Round306C30q compact-q zero-credit research checkpoint

Date: 2026-08-08

## Formal boundary

This document is research-only.  It changes no Source-W ledger, grants zero
formal credit, authorizes no seal or release, and leaves all 54 compact-q
origins formally remaining.  D02 remains blocked and CM2 remains
`NO-GO_FOR_CLAIM`.

## Frozen authority and counterexample boundary

- Round218 remains the compact-q authority: 54 outcome-blind origins, 844
  initial q roots, zero whole-origin credit.
- C30q0 proves one North representative whole-origin theorem with independent
  verification and attacks.
- C30q1-v3 gives an exact strict-interior counterexample to automatic extension
  of the representative frozen-behind sufficient subclaim.  It is not a CM2
  counterexample and does not identify an alternative first owner.
- C30q2 exhaustively routes 54 origins into seven exact patterns.  Only six
  origins have all analytic roots applicable.  The old combined gate accepted
  two because it additionally required exactly one complement residual.

## C30q3: independent South paired theorem

The South origin `W:S:H.03.15.01111111` is proved directly, without inferring
geometry from the observed North/South key pairing:

- 16 full-r analytic root domains;
- 255 cross-root relative-open strata;
- dimension census `3D/2D/1D/0D = 16/74/111/54`;
- frozen forward projection strictly below `-1/2`;
- nonfrozen future projection strictly above `15857/32000`;
- transverse margin strictly above `13/500`;
- 10 of 10 coherent attacks rejected.

Durable receipt:

`.cm2-runtime/audit/c30q3-south-theorem-zero-credit-v1-20260808T064505Z/receipt.json`

Root manifest SHA-256:

`fb479b15280a3027f702896470475b0cb3c16a0970d70f6dbfcde5964aa646df`

## C30q4: exact-one-residual condition is unnecessary for two origins

C30q4 targets the North/South `03.15.11010111` pair.  It replays the actual
Round176 -> Round180 -> P215 complement and tests universal containment rather
than requiring exactly one residual.

For each origin:

- `62 = 7 preclosed + 55 unresolved` Round176 frontier roots;
- 548 Round180 children;
- 420 P215 exact-behind closed children;
- 128 surviving children, all compact-q;
- all 128 survivors lie in exactly one of 16 full-r analytic roots;
- all 16 analytic roots certify frozen-behind plus a `W[-1,0]` future witness;
- all 255 cross-root strata are owned exactly once.

Combined result:

- 32 of 32 analytic roots pass;
- 256 of 256 residual children pass universal containment;
- producer result SHA-256
  `729d1dc2cef3b35e9c9d8d1e3a45787189c1169130c321d6ac01d6c1572ad188`;
- independent verifier passes;
- 12 of 12 coherent attacks are rejected.

Durable recovered receipt:

`.cm2-runtime/audit/c30q4-11010111-universal-containment-zero-credit-v1-20260808T070947Z/receipt.json`

Root manifest SHA-256:

`29c1616561a43ee77a1407d039a89f8a4a064b9d57b8674ca1bca6ab86a6ae5f`

The receipt explicitly records that the original audit wrapper completed all
five computational stages with numeric exit zero, then hit a shell quoting
parse failure while finalizing its receipt.  An independent finalizer checked
the retained outputs and original pre-snapshot, then emitted the recovered
receipt.  It also records that both producer stderr files contain the same
43-byte progress line.  Therefore this is not an empty-stderr formal-promotion
artifact.

## Next falsifiable gate

Target the remaining fully-analytic `03.15.11010101` North/South pair.  Each
has 136 complement residuals:

- 128 compact-q residuals, to be tested by the now-validated universal
  containment criterion;
- 8 `CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH` residuals, which need
  their own exact graph/half-open ownership theorem.

The two categories must remain separate.  A pass on the 128 compact-q rows
does not close the eight clipped rows, and neither result grants formal credit.
