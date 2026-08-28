# CM2 Round 114 — seam/root stitch and fail-closed collar gap atlas

Date: 2026-07-23  
Verdict: **VERIFIED selected-lift trace coverage; the physical collar remains open.**

## What Round114 pays

Round114 closes the first of the three Round111 residual objects outright and
replaces the other two by the legal Round112 blown-up endpoint coordinate.

1. **Eight source-chart transfer seam brackets are physically bridged.**
   Each positive-width bracket is replayed in Cartesian geometry while the
   source owner comparison is checked against the union of the `E/W/N/S`
   first-hit tables.  The selected reverse path and all first, second, and
   third competitor exclusions have a common strict lower margin.  Across the
   eight rays the seam widths range from about `3.15e-38` to `9.79e-37`, while
   the smallest selected-flight/competitor margin is greater than `0.0019`.

2. **The finite pre-root tail is covered to the unique blown-up corner.**
   On the shared `c3=b3=0` edge of each Round112 HIT/BYPASS pair, the equation

   ```text
   Delta3(t,c0) = 0,       0 <= c0 <= 1/16384
   ```

   has a unique continuous `t(c0)` graph because the valid blown-up
   determinant is

   ```text
   det D_(c0,t)(c0,Delta3) = partial_t Delta3,
   |partial_t Delta3| > 3.
   ```

   The stereographic projective coordinate of the selected second outgoing
   direction is well defined on the whole enclosing edge box; its denominator
   has a uniform lower bound greater than `0.019`.  At `c0=1/16384` its image
   lies strictly before the last unresolved Round111 tail by at least
   `1.46e-11` on every ray.  At `c0=0` it lies strictly inside the tight Round94
   root enclosure.  Continuity and the intermediate-value theorem therefore
   cover the pre-root tail and reach the unique corner on all eight rays.

3. **The endpoint contract is corrected.**  The tight grazing bracket is a
   numerical enclosure of one unknown endpoint.  It is not a physical trace
   interval whose every parameter must be covered.  Round114 proves that the
   unique corner is inside that enclosure; it does not claim coverage of the
   parameter values on the nonphysical side of the endpoint.

The resulting selected-lift algebraic trace coverage is **8/8**.

## What remains open

The preceding `8/8` statement is intentionally separated from every stronger
physical or operator claim:

- physical-owner trace closure: **0/8**;
- injective/no-fold whole-trace atlas: **0/8**;
- uniform positive normal reach: **0/8**;
- uniform distance from every other singularity and representation seam:
  **0/8**;
- two-sided physical whole-trace collar: **0/8**;
- whole-collar 57-candidate ordering: **0/8**;
- new actual-child Gate5 fields: **0**.

The IVT argument supplies image coverage only.  It does not prove that
`q(c0)` is injective, and it cannot substitute for a reach or no-fold theorem.
The Round112 root edge still has only selected-collision geometry: complete
first/second owner order and the 57-candidate third comparison remain open.
HIT and BYPASS are separate real sheets and share only `c3=b3=0`.

## Shortest remaining proof chain

1. Replay the complete owner/candidate tables on every HIT and BYPASS root
   sheet; indeterminate comparisons must split the sheet and remain residual.
2. Prove the root-edge fold law/no-extra-turn property (or install an equally
   rigorous injective transition atlas) so that the endpoint overlap has a
   unique coordinate crosswalk, not merely IVT coverage.
3. Thicken the certified middle trace in verified normal boxes and prove a
   uniform positive reach, transition-map uniqueness, and positive distance
   from all other collision singularities, wall corners, caps, and seams.
4. Only then install the exact countable homogeneity partition and recut the
   actual curves along the official word before paying child-keyed `F1–F6`.

## Independent verification

- producer replay: **640 bits**;
- independent verifier replay: **768 bits**;
- Round114 producer imported by verifier: **false**;
- exact seam-union replays: **8/8**;
- high-precision seam-union replays: **8/8**;
- exact root-edge endpoint/order/denominator/determinant replays: **8/8**;
- high-precision root-edge replays: **8/8**;
- semantic hostile mutations rejected: **13/13**;
- duplicate-key, nonfinite, and unknown-top-level JSON attacks rejected:
  **3/3**.

The verifier byte-pins every direct geometry helper it imports and requires
the certificate's complete upstream/helper pin map to equal the producer's
hard-coded map.  CM2 remains **`NO-GO_FOR_CLAIM`**.
