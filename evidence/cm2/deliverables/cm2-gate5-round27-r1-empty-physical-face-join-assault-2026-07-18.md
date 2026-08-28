# CM2 Gate 5 — Round-27 R1 empty physical-face join

Date: 2026-07-18  
Status: append-only strict leaf; aggregate and recursive root untouched

## Frozen conclusion

The round-26 F10/F13 obstruction is resolved on the **4,216 strict R1-inner
atoms themselves**.  The resolution is not an occurrence-level seed copied
onto artificial faces.  It is an exhaustive proof that the physical
collision-occurrence face family intersecting every such atom is empty.

Consequently this leaf installs

```text
F10 empty physical-coarea-family slots       4,216
F13 empty moving-current/trace-family slots  4,216
                                                -----
new immutable candidate-local slots          8,432
```

Candidate-local maturity rises from `11/18` to `13/18`.  The limiting R1
physical boundary atlas, F14--F18, complete blocks and global Gate 5 remain
open.  Global Gate 5 therefore stays `4/18`, `NOT_CERTIFIED`, and CM2 remains
`NO-GO FOR CLAIM`.

## 1. Physical carrier replay

The producer independently replays all frozen physical inputs:

```text
maximal moving collision-occurrence rows       64
physical hit trace seeds                       64
physical miss trace seeds                      64
distinct oriented trace seeds                 128
```

Every occurrence row is a first-event grazing carrier.  On its event target,
the collision coordinate is exactly

```text
p_target = epsilon in {-1,+1}, hence |p_target|=1.
```

The corrected positive coarea law and its nonzero density continue to belong
to those 64 physical carriers.  Nothing in this leaf retypes a dyadic box face
as one of them.

## 2. Exact 4,216 x 64 disjointness audit

Each R1-inner atom inherits a frozen compact source core.  Every source core
has been replayed against the complete retained collision candidate list and
satisfies, uniformly on the full parameter window,

```text
selected collision is the strict first hit,
incoming and outgoing |p| < 3/10,
incoming and outgoing cos(phi) > 19/20,
branch-internal singularity cut count = 0.
```

The producer classifies all

```text
4,216 * 64 = 269,824
```

atom/occurrence pairs.  The exact trichotomy is

```text
different collision-section component                         133,568
same component, different first target                         106,520
same first target, grazing |p|=1 versus core |p|<3/10           29,736
                                                               -------
total                                                          269,824
```

The first class is disjoint by collision-section typing.  In the second
class, a state cannot simultaneously have the core's strict selected first
target and the occurrence row's different first-event target.  In the third
class, the common target still has the strict coordinate gap

```text
1 - 3/10 = 7/10.
```

Thus the certified physical intersection count is exactly zero.  This is an
empty join, not an unavailable join.

## 3. F10: empty physical coarea family

For each atom the F10 slot contains the complete 64-row occurrence universe,
an empty list of intersecting occurrence IDs, and the three-way disjointness
proof above.  Its branch-local coarea-density regularity cost is the empty sum

```text
F10 cost = 0.
```

The global occurrence magnitude seed `18/5` is not copied onto the atom.  The
16,864 fixed-coordinate R1 face incidences are recorded but explicitly
excluded from the physical carrier type.

## 4. F13: empty moving current and empty trace-pair family

On the same fixed R1-inner restriction, the intersecting physical moving-face
family is empty.  Therefore the branch-local face current is zero and its
hit/miss trace families are both empty:

```text
physical face count       0
moving face current       0
hit trace seed count      0
miss trace seed count     0
trace-pair count          0
```

The assertion that every intersecting physical face has one hit and one miss
trace is vacuous on this **certified empty** family.  It is not an assertion
that the smooth branch derivative vanishes; that derivative remains carried
by the already frozen F11 smooth pullback field.

## 5. Why this does not close the global physical face problem

The 4,216 atoms are strict interior rectangles, not a face complex for the
limiting R1 set.  Differentiating a completed return operator still requires
the nonempty singular and destination-core preimage faces that occur at the
boundary of that limiting partition, together with common subdivisions,
quotient trace assembly and return-wide norms.  This leaf therefore does not
claim any of the following:

- a limiting-R1 physical boundary face atlas;
- transported occurrence-to-24-core recovery incidence;
- the global depth-one DQ current from an empty local current;
- F14 regular-density, F15 standard-family, F16 flux-face, F17 dynamic-test,
  or F18 phase-block costs;
- a complete 18-field R1 block, induced strong Lasota--Yorke coefficient, or
  Gate-5 credit.

The next missing candidate-local field is F14
`regular_density_operator_cost`, but it cannot be filled from inner-box empty
faces alone.

## 6. Exact nonpromotion boundary

```text
R1 F10 CANDIDATE-LOCAL SLOTS:                         4,216
R1 F13 CANDIDATE-LOCAL SLOTS:                         4,216
R1 CANDIDATE-LOCAL MATURITY:                          13/18

INTERSECTING ATOM/OCCURRENCE PAIRS:                       0
ARTIFICIAL R1 FACES USED AS PHYSICAL CARRIERS:         FALSE
LIMITING R1 PHYSICAL BOUNDARY ATLAS:          NOT CERTIFIED
F14--F18:                                     NOT CERTIFIED
COMPLETE 18-FIELD R1 BLOCKS:                              0
GLOBAL GATE-5 MATURITY:                     4/18 UNCHANGED
GATE 5:                                       NOT CERTIFIED
CM2:                                      NO-GO FOR CLAIM
```

## 7. Replay and hostile verification

Artifacts:

- `cm2_gate5_round27_r1_empty_physical_face_join_cert.py`
- `cm2_gate5_round27_r1_empty_physical_face_join_verifier.py`
- `cm2-gate5-round27-r1-empty-physical-face-join-manifest-2026-07-18.json`
- `cm2-gate5-round27-r1-empty-physical-face-join-manifest-2026-07-18.sha256`

The frozen result replay digest is

```text
4a2457f6c86aa02f7885a4fe2f4908a2e14ef06d03798d0ba05d936263545580.
```

Reproduction:

```bash
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate5_round27_r1_empty_physical_face_join_verifier.py \
  --integrity-only

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate5_round27_r1_empty_physical_face_join_verifier.py \
  --replay

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate5_round27_r1_empty_physical_face_join_verifier.py \
  --self-test
```

Integrity and full replay pass.  Hostile tests pass `83/83`.  Default live
mode exits `2`, preserving the fail-closed limiting-face, F14--F18, Gate-5 and
CM2 status.
