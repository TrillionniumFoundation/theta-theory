# CM2 Gate 4/5 round-29 Q2 seam, recut-instance and face frontier

Date: 2026-07-18  
Status: append-only strict leaf; round 28, aggregates and recursive roots untouched

## Frozen verdict

This leaf makes one finite geometric advance and freezes two exact type
blockers.

First, it replays the complete 416,994-leaf time-two registry at 384-bit Arb
precision and fairly refines exactly the 5,280 strict Q2 boxes that did not
strictly exclude the time-two target normal-chart seam.  Six additional
dyadic levels produce

```text
refined terminal cells                         170,394
new strict-single-chart children                62,358
residual representation-seam outer cells       108,036
```

The residual *count* grows because a codimension-one tube is being covered by
smaller boxes.  The relevant exact mass drops from

```text
524111/5120000000
```

to

```text
1819573/327680000000.
```

Equivalently the residual ratio is

```text
1819573/33543104 < 1/18,
```

so more than `17/18` of the old seam-frontier coordinate-base mass is now in
strict single-chart cells.  This is a finite-depth result, not an iterated
boundary-tube theorem and not a complete chart atlas.

Second, the leaf keeps the two missing object layers strongly separated:

```text
canonical-recut branch-rule IDs                228,012
actual parent-W curve-instance IDs                   0
instantiated connected physical face pieces          0.
```

The first true recut blocker is the absence of a materialized
parent-canonical-`W` registry on the Q2 strong restriction.  A branch rule is
not silently promoted to an actual
`(branch-rule-id,parent-W-id,natural-index-j)` curve instance.

Therefore Q2 F7 and F14--F18 remain `NOT_CERTIFIED`, global Gate 5 remains
`4/18`, and CM2 remains `NO-GO FOR CLAIM`.

## 1. Full replay and inherited Q2 scope

The producer reconstructs the frozen 2,868 Q1 parents, reruns the complete
time-two recursion and obtains the exact round-28 ledger:

```text
terminal leaves                              416,994
strict Q2-inner atoms                        114,006
time-two unresolved outer leaves             302,988
Q2 coordinate-base mass       5257799/5120000000.
```

Every refined child is a subset of a strict Q2-inner parent.  The strict
outside-of-C24 statement is therefore inherited.  The two collision owners
are nevertheless freshly replayed on every refined child because the target
normal chart is an owner-coordinate object, not a label inherited from the
source box.

The refinement is fair in the same normalized `(t,p,s)` box scales as the
frozen adaptive recursion.  It stops as soon as one of `E/N/S/W` is strictly
isolated, or at additional depth six.  The exact depth histogram is

```text
additional depth 1       1,722
additional depth 2       2,602
additional depth 3       5,820
additional depth 4       7,154
additional depth 5      12,912
additional depth 6     140,184.
```

All child-parent prefix ownership and each parent mass split are exact.  The
global identity is

```text
31723531/327680000000 + 1819573/327680000000
  = 524111/5120000000.
```

The pre-existing 108,726 strict-chart Q2 atoms plus the 62,358 new refined
strict-chart cells give a mixed-resolution strict F4 subledger of 171,084
cells.  The 108,036 residual boxes receive no F4 chart claim.  A normal-chart
seam remains a representation boundary and is never charged as a physical
singularity or physical face.

## 2. Actual parent-W recut-instance blocker

Round 28 certified two immutable branch rules per strict Q2 atom.  Their
universal F5/F6 estimates quantify every eventual canonical curve instance,
but the rule does not identify any such instance.  An actual instance needs
all three entries

```text
(branch-rule-id, parent-canonical-W-id, natural-index-j).
```

The frozen Q2 dependencies contain no parent-canonical-`W` registry on the
same forward/reverse restriction.  Consequently this leaf freezes

```text
actual parent-W registry count                         0
actual curve-recut instance-ID count                   0
actual instance characteristic-Z/F7 charge count       0.
```

This is not a statement that no canonical unstable curve exists.  It is the
strict typed statement that no actual Q2 curve-instance registry has been
materialized and joined.  In particular, the 228,012 branch rules are not
counted as curve components, and no artificial dyadic endpoint is charged as
a physical cut.

## 3. Terminal C24 face family audit

At the second collision only the 12 cores on the selected target obstacle are
compatible, hence there are 48 terminal core-face families per Q2 atom.  The
fresh strict-Q2 replay gives

```text
114006 * 48 = 5,472,288
```

atom/family pairs.  Every pair is empty on the strict Q2-inner whole box.  For
each compatible core the Q2 classifier has a whole-box strict separator from
the closed core rectangle; the same separator excludes all four bounded
faces of that rectangle.

This certified-empty terminal family is useful bookkeeping, but it does not
materialize a connected face piece or a connected rank.  It also does not
cover source clipping, intermediate avoidance/owner-change carriers,
physical word boundaries, or moving-occurrence pullbacks.  Therefore it is
not promoted to a complete Q2 physical face atlas, a numerical
transversality/coarea/one-sided-trace theorem, or an F14--F18 operator block.

The following namespaces remain disjoint:

- branch rules versus actual parent-`W` recut instances;
- carrier families versus connected one-dimensional face pieces;
- artificial dyadic faces versus physical collision faces;
- target normal-chart seams versus physical singularity cuts;
- empty terminal families versus a complete limiting physical face atlas.

## 4. Exact Gate-5 frontier

The new strict conclusion is

```text
F4 strict-single-chart subledger        ENLARGED BY 62,358 CELLS
F4 complete Q2 chart ledger             NOT CERTIFIED
F7 actual-instance Z slots              0
connected physical face-piece IDs       0
numeric nonempty-face coarea/trace       NOT CERTIFIED
F14--F18 materialized slots              0
complete 18-field operator blocks        0
global Gate-5 maturity                   4/18 UNCHANGED
CM2                                      NO-GO FOR CLAIM.
```

The shortest next interface is now explicit:

1. build a parent-canonical-`W` registry on the same Q2 forward/reverse
   restriction and instantiate the natural-index recut cells;
2. charge the resulting real recut endpoints and word boundaries in F7;
3. continue fair seam refinement or prove a limiting chart-tube theorem;
4. parameterize every nonempty physical carrier intersection, assign its
   connected rank, and certify numeric transversality, coarea and one-sided
   trace bounds;
5. only then assemble F14--F18 on the same branch/restriction IDs.

## 5. Verification

Artifacts:

- `cm2_gate45_round29_q2_seam_recut_face_frontier_cert.py`
- `cm2_gate45_round29_q2_seam_recut_face_frontier_verifier.py`
- `cm2-gate45-round29-q2-seam-recut-face-frontier-manifest-2026-07-18.json`
- `cm2-gate45-round29-q2-seam-recut-face-frontier-manifest-2026-07-18.sha256`

The fail-closed verifier checks dependency and artifact integrity, exact count
and mass identities, prefix/depth/chart ledgers, the zero-instance and
zero-connected-piece type barriers, and all nonpromotion fields.  Its replay
mode independently reruns the full 384-bit Arb construction.  Live mode exits
`2` by design because CM2 remains unavailable.
