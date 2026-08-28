# CM2 Round 92 — centered-Taylor closure of the exterior-ray residuals

## Result

Round 91 certified 61 of the 65 live exterior projective rays to their first
frozen source-core boundary.  Four interval chains stopped because the direct
competitor-root calculation returned an interval discriminant containing zero.

Round 92 first evaluated every translated competitor at 512 point states along
each residual ray.  No competitor discriminant changed sign.  The closest
strict point margins were of order `0.001064` or `0.001545`, so the Round 91
failure was interval dependency rather than a physical competitor-grazing
event.

The formal repair evaluates each competitor discriminant in the source
coordinates `(t,p)` by a centered first-order Taylor enclosure:

```text
D(B) ⊂ D(c) + D_t(B)·[-r_t,r_t] + D_p(B)·[-r_p,r_p].
```

The repaired classifier retains the complete translated candidate table and
recomputes every real competitor's near root and its strict order relative to
the designated tangent target.  It is used only when the original direct
interval classifier reports `unresolved_discriminant`.

All four residual rays close:

| Core | Branch target | Projective end | Strips | Taylor repairs |
|---:|---|---|---:|---:|
| 12 | `G[3,-1]`, sign `+1` | left | 32,768 | 2,186 |
| 13 | `G[3,2]`, sign `-1` | right | 32,768 | 2,593 |
| 14 | `W[-2,1]`, sign `+1` | left | 65,536 | 0 |
| 16 | `G[2,3]`, sign `+1` | left | 32,768 | 5,396 |

The core-14 row needs 65,536 strips; at that resolution the original direct
interval discriminants are already strict, hence its Taylor-repair count is
zero.

Combined with Round 91, all `65/65` exterior rays are now certified as physical
next-tangency branches until their first frozen source-core boundary.  The
unresolved exterior-ray count *inside the frozen source cores* is zero.

## Strict interpretation

This closes the projective continuation problem only on the frozen source-core
registry.  A source-core boundary is an artificial registry boundary, not a
global physical-face endpoint.  Round 92 therefore does not install a complete
physical-face quotient, RN rows, Gate 5 fields, or any global gate.

The strict global state remains:

- Gate 1: `NOT_CERTIFIED`;
- Gate 2: `0/17`;
- Gate 3: `NOT_CERTIFIED`;
- Gate 4: `1/7`;
- Gate 5: `10/18`, complete blocks `0`;
- composite gates: `0/5`;
- CM2: `NO-GO_FOR_CLAIM`.

## Next frontier

The next rank-three task is to continue the 65 frozen-core exits into the full
physical source chart until each branch reaches a true source exit,
owner/chart/translation seam, or genuine rank-transition event.  Only after
that continuation can the complete physical-face quotient and RN frontier be
rebuilt.

