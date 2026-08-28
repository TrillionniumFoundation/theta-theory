# CM2 Eighty-Sixth Direct Assault — 2026-07-22

## Scope

Round 86 performs the finite refinement explicitly exposed by the Round-85
C24 variable-return crosswalk.  It attacks both the 32 reached
`UNRESOLVED_OUTER` target atoms and the 2,328 return landings whose interval
enclosures straddle frozen target-leaf boundaries.  It preserves exact
rational mass ledgers and does not reinterpret containment as recurrence or a
stable plaque.

## Reached unresolved targets

The 32 unique reached unresolved atoms are refined for 12 normalized
longest-axis levels.  Each child is replayed through the frozen physical
classifier.  The final exact partition is

```text
input unresolved parents                              32
final leaves                                        2980
SURVIVE_THROUGH_1_INNER leaves                      2732
UNRESOLVED_OUTER residual leaves                     248
residual volume ratio                           31/16384
```

The child volumes sum exactly to the parent volume.  Thus this finite attack
removes more than `99.8%` of the original unresolved volume, but it does not
close the remaining 248 leaves or manufacture a later return.

## Boundary-straddling landing preimages

The 2,328 return-source parents not already certified as wholly contained in
one frozen target leaf are split for three levels.  At every level the full
landing interval is recomputed and accepted only when it lies strictly inside
one target atom in all coordinates.  The final exact cover is

```text
boundary-straddling parents                         2328
strictly contained children                         1304
residual children                                  15344
residual volume ratio                           1991/2298
```

Resolved-child plus residual-child volume equals the input volume exactly.
The large residual ratio is diagnostic: the frozen source-leaf partition and
the pullbacks of landing target boundaries are systematically misaligned.
Blindly adding longest-axis dyadic depth is therefore not the shortest route.
The next generator should isolate the exact pullback boundary equations and
cut along them before re-running strict target containment.

## Verification

The producer runs at 512-bit precision.  The independent verifier recomputes
the two refinements at 768 bits, validates both mass-preserving covers, pins
the full-core atlas, C24 registry source, and Round-85 crosswalk, and rejects
all four configured hostile mutations.  The frozen audit status is
`AUDIT_PASS`.

## Strict state and next frontier

No `RETURN` edge, recurrent component, or same-key all-depth root is created.
Interval-possible graph containment is not called a stable plaque.  Therefore

```text
Gate 1                         NOT_CERTIFIED
Gate 2                         0/17
Gate 3                         NOT_CERTIFIED
Gate 4                         1/7
Gate 5                         10/18, complete blocks 0
complete composite gates       0/5
CM2                             NO-GO_FOR_CLAIM
```

The shortest remaining C24 attack is an exact landing-pullback arrangement:
isolate source boxes where landing `t`, `p`, or `s` equals a frozen target
boundary, split the 2,328 parents by those certified curves/surfaces, and only
then search the resulting variable-return graph for nonempty recurrent
same-key subroots.

