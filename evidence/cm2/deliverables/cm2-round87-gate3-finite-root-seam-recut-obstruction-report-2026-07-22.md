# CM2 Round 87: finite-root Gate 3 seam recut obstruction

## Certified result

The remaining Round-85 finite-root Gate 3 gap cannot be repaired by an exact
repartition of the current frozen registry.  On every immutable directed
physical branch, subdivision preserves the positive-side and negative-side
unions.  Each of the 24 unmatched positive owner rectangles and 24 unmatched
negative rectangles meets the opposite union only in a set of two-dimensional
measure zero.

The exact closure-contact census over the 48 rows is:

- 40 edge-seam rows and 8 corner-only rows;
- 64 edge contacts and 48 corner contacts;
- 40 edge contacts normal to `t` and 24 normal to `p`;
- tangential widths: 40 contacts of width `1/800`, 24 of width `1/3200`.

Thus a finite exact recut leaves the Round-85 coverage at `152/176`.  Closing
an edge-seam row requires a positive-width collar across at least one normal
coordinate.  Closing a corner-only row requires a positive-area neighborhood
across both coordinates.  Any such enlargement must receive fresh proofs of
the immutable branch key, strict first owner, flight order, and destination
core; it is not a mere repartition.

## Verification

All 48 boxes were replayed as `RETURN_AT_1_INNER` to their frozen destination:
512-bit Arb in the producer and an independent 768-bit replay in the verifier.
The verifier also independently rebuilt all exact rational contacts, required
fresh producer equality and a closed JSON schema, and rejected 6/6 semantic
mutations, 8/8 coordinated pin mutations, and 4/4 strict-JSON attacks.

## Scope

This is a sharp obstruction for the current finite `s=0` registry only.  Gate
3 remains uncertified.  No global two-sided trace/current atlas, all-depth
Piola recipient, or stopped `MT_DQ` estimate is promoted.  A newly enlarged
registry is not excluded, but it must carry new owner/flight proofs.
