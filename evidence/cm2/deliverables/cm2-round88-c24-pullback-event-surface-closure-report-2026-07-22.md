# CM2 Round 88: C24 pullback event-surface closure

## Result

The 6,952 positive-volume boxes left by Round 87 are no longer a
positive-volume landing-to-leaf ambiguity.  On every box, every frozen target
leaf face that the landing enclosure can meet is the zero set of a regular
event function.  The finite union of these transverse event hypersurfaces is
Lebesgue null.  Away from it, the frozen 33,960-leaf atlas assigns a unique
target leaf.

This is an almost-everywhere crosswalk closure.  A point lying exactly on a
shared closed leaf face is deliberately not assigned a canonical leaf.

## Certified event sweep

- Round-87 residual boxes: **6,952**, from **1,952** parent return atoms.
- Residual volume: `1793/8192000000`; ratio: `1793/2298`.
- Frozen target coordinate-boundary values over all cores:
  - `t`: 424
  - `p`: 296
  - `s`: 536
- Box-local boundary-event occurrences: **95,436**:
  - `landing_t = b_t`: 73,396
  - `landing_p = b_p`: 2,776
  - `s = b_s`: 19,264
- Interval-AD transverse derivative witnesses:
  - `landing_t` by source `t`: 73,280
  - `landing_t` by source `s`: 116
  - `landing_p` by source `t`: 2,776
  - `s` by source `s`: 19,264
- Every `landing_t/p` witness has absolute partial derivative strictly greater
  than `7/5`; every `s` event has derivative exactly `1`.
- Every source chart radical, momentum radical, collision discriminant, flight
  order, destination chart, and destination-core interior test is strict on
  each box.

The occurrence count is a box-local certificate census.  It is not presented
as the number of globally distinct hypersurfaces.

## Same-key recurrence search

All 6,952 landing `p` enclosures are strictly outside the destination core's
union of frozen `RETURN_AT_1_INNER` source atoms, using a uniform coordinate
gap greater than `1/200`:

- below the RETURN-source hull: 3,476
- above the RETURN-source hull: 3,476

Together with the pinned Round-85 all-4,216-atom empty incidence graph, this
certifies zero one-step `RETURN -> RETURN` edges and no nonempty one-step
recurrent same-key subroot in the current frozen atlas.

This does not exclude a later return through survivor leaves, a different C24
subroot, or a larger landing registry.

## Verification

- Producer precision: 512 bits.
- Independent verifier precision: 1,024 bits.
- The verifier separately implements interval forward differentiation and
  recomputes all 6,952 rows and all 95,436 box-local event occurrences.
- Semantic mutations rejected: 8/8.
- Dependency-pin mutations rejected: 11/11.
- Strict-JSON attacks rejected: 4/4.
- Producer and verifier cold replays match their frozen JSON byte-for-byte;
  both stderr streams are empty.
- Both Python sources parse and compile; all four primary artifacts are
  nonempty, valid, and contain no zero bytes.

Primary SHA-256 values:

```text
2e5f7f303745c556c211e29f04d2377fa493db3b04e7ffca078295cc91d0bc58  cm2_round88_c24_pullback_event_surface_closure_cert.py
d5f44e0ee65f06cb7d573b16737475bf89f186b28dc79c38d26aafbb1219f4eb  cm2-round88-c24-pullback-event-surface-closure-2026-07-22.json
ac5c739c34b5ce5097c4aeaebff6174bcb0ac42f5306e2c7e4a5af537f5f4eb3  cm2_round88_c24_pullback_event_surface_closure_verifier.py
4b531d20b586fce7201b46b6278a8f21c8ee90c8c1daa852422e84f1219f1b75  cm2-round88-c24-pullback-event-surface-closure-audit-2026-07-22.json
```

## Lawful gate state

- Gate 2 remains `0/17`.
- Gate 4 remains `1/7`.
- No stable plaque, physical holonomy, later-time return path, or all-depth
  same-key stable/material crosswalk is installed.

