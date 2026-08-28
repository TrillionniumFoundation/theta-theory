# CM2 Gate 5 — Round-26 R1 F10--F13 typed frontier

Date: 2026-07-18  
Status: append-only strict leaf; aggregate and recursive root untouched

## Frozen conclusion

The 4,216 strict full-dimensional R1 candidate atoms admit two further
independent candidate-local Gate-5 fields:

```text
F11 dynamic_Holder_test_pullback_bound     4,216 slots
F12 C1_face_trace_pullback_bound           4,216 slots
                                               --------
new immutable candidate-local slots        8,432
```

After the exact atom/homogeneity join to the frozen F1--F9 companions, the
candidate-local maturity is therefore `11/18`.  The field order is not being
silently changed: F10 remains absent, F11 and F12 are installed independently,
and F13--F18 remain absent.

The first unfillable field is exactly

```text
F10 coarea_density_regular_bound: NOT_CERTIFIED.
```

This local `11/18` adds no global Gate-5 credit.  The 4,216 atoms are still an
incomplete R1 candidate subcover, complete 18-field blocks remain zero, and
global Gate 5 stays `4/18`, `NOT_CERTIFIED`.

## 1. Exact input join

The producer replays the complete 26 MB round-25 F1--F6 packet registry, the
F7--F9 face registry, the 24-core producer itself, and the frozen F10--F13
schema.  All 4,216 atom IDs and all 4,216 physical homogeneity IDs are unique.
The atom digest agrees exactly with the F7--F9 companion:

```text
db9fbc97e5528f13d0e330b8905777d1128e9f99a4d4766b1020331efaea5faf.
```

Every row has roof one, one central `H0 -> H0` collision child, a positive
owned `(t,p,s)` box, and four fixed-fibre coordinate faces.  There are 16
source and 16 destination cores among the retained rows.

The physical-core producer is replayed rather than trusted only through its
summary.  On all 24 compact cores it verifies

```text
||DF_s||_infinity, ||DF_s^-1||_infinity < 158,
C^alpha target-test pullback cost < 158,  0<alpha<=1.
```

No collision-area Jacobian is used in either new field.

## 2. F11: fixed-s dynamic-Hölder pullback

Fix `s` in one atom's owned parameter interval.  Restricting a smooth compact
one-collision branch to a smaller owned rectangle cannot worsen its already
certified target-test pullback bound.  Each atom therefore receives one F11
slot with

```text
fixed-s C^alpha pullback cost < 158,  0<alpha<=1.
```

The half-open parameter guard only selects the fibre.  This field does not
differentiate a guard endpoint and is not a return-wide dynamic-test operator
cost.  The combined F11/F12 immutable slot-ID digest is

```text
2c7de87ed6cf3c73e0bc8ca66e7d1b46e936ec36747e9530621087a2556a8a29
```

with combined slot-row digest

```text
17ec6eef1e6a63cf001cb231bb1116626f249863213f275fc0f67ba8f753c580.
```

## 3. F12: four fixed-fibre C1 trace bounds

The F7--F9 leaf already registered four unit-speed coordinate faces on every
atom.  The present replay reconstructs exactly the same face IDs and face-row
digests.  For a target test `Phi` and a unit face tangent `e`, the chain rule
gives

```text
||Phi o F_s||_infinity <= ||Phi||_infinity,
|d(Phi o F_s)(e)| < 158 ||D Phi||_infinity.
```

Thus the usual sum `C1` norm has strict multiplier `<159` on each individual
face.  Corners are endpoints, not additional C1 faces.  This is an analytic
fixed-s trace-pullback field; it does not attach a physical hit/miss current
or claim the still missing coincident-face assembly.

## 4. Why F10 cannot be filled

The frozen physical occurrence current has 64 maximal moving collision faces,
with corrected law

```text
dm_e = R_source*cp*abs(u_y)/ell_T dtheta,
```

and magnitude upper `18/5`.  Its oriented density-regularity costs are

```text
|d log rho_rev/dr_source| < 27*2^B,
|d log rho_fw/dr_miss|    < 52*2^B.
```

Those are genuine one-collision physical inputs, but they live in the
occurrence namespace: each uses an occurrence-specific endpoint rank `B` and
source/miss carrier.  The R1 registry instead has

```text
4*4216 = 16,864
```

artificial fixed-s coordinate-face incidences.  The materialized join

```text
(occurrence_id, endpoint rank, oriented carrier)
    -> (R1 atom_id, homogeneity_id, phase_face_id)
```

has count zero.  Consequently:

- `18/5` cannot be copied from a physical occurrence face and called an R1
  density-regularity field; it is only a magnitude upper on the wrong carrier;
- the `27*2^B` and `52*2^B` bounds cannot be used without the missing rank and
  carrier join;
- the artificial face coordinates are constant in `s`, but assigning density
  zero from that coordinate speed would confuse a bookkeeping cut with the
  positive coarea law of a moving collision occurrence; and
- the R1 candidate subcover is incomplete, so internal artificial faces have
  not undergone the required common subdivision and quotient-trace assembly.

This is a type obstruction, not evidence that a correct physical F10 bound is
false.  It precisely identifies the next object that must be built.

## 5. Why F13 cannot be filled by half-open guards

There are 48 distinct R1 parameter intervals.  Their exact audit gives

```text
guards touching s=0:                     352
guards owning s=0 by half-open rule:     176
guards with s=0 in relative interior:      0
```

The frozen complete transfer DQ theorem is based at `s=0` and has 64 physical
occurrence faces, each with a hit trace and a miss trace.  No R1 parameter
guard supplies an open two-sided neighbourhood of that base point, and no
occurrence hit/miss trace has been joined to an R1 face ID.

A half-open guard endpoint is an ownership convention, not a row of the
moving-boundary DQ atlas.  Likewise the zero fixed-section coordinate speed of
an artificial phase face is not the physical DQ current.  The older statement
that chart/lift artificial currents vanish applies after global quotient trace
assembly; that assembly is unavailable on the incomplete R1 candidate
subcover.  Therefore F13 remains strictly `NOT_CERTIFIED`.

## 6. Downstream F14--F18 frontier

The first missing dependency of each remaining field is frozen explicitly:

- F14 needs a complete branchwise regular-density cost including F10;
- F15 needs union-wide F7 plus density/recovery control, not per-atom seeds;
- F16 needs assembled physical flux faces with F10, F12 and F13;
- F17 needs return-wide dynamic tests and the physical F13 current;
- F18 needs a complete operator block before phase registration.

No F14--F18 slot and no phase block is materialized.

## 7. Exact nonpromotion boundary

```text
R1 F11 CANDIDATE-LOCAL SLOTS:                         4,216
R1 F12 CANDIDATE-LOCAL SLOTS:                         4,216
R1 CANDIDATE-LOCAL MATURITY AFTER JOIN:               11/18

F10 COAREA-DENSITY REGULARITY:                NOT CERTIFIED
F13 MOVING-BOUNDARY DQ + TWO TRACES:          NOT CERTIFIED
F14--F18:                                     NOT CERTIFIED
COMPLETE 18-FIELD R1 BLOCKS:                              0
GLOBAL GATE-5 MATURITY:                     4/18 UNCHANGED
GATE 5:                                       NOT CERTIFIED
CM2:                                      NO-GO FOR CLAIM
```

## 8. Replay and hostile verification

Artifacts:

- `cm2_gate5_round26_r1_f10_f13_frontier_cert.py`
- `cm2_gate5_round26_r1_f10_f13_frontier_verifier.py`
- `cm2-gate5-round26-r1-f10-f13-frontier-manifest-2026-07-18.json`
- `cm2-gate5-round26-r1-f10-f13-frontier-manifest-2026-07-18.sha256`

The result replay digest is

```text
2ef722e84b000768d2d598eeb600bf94319bda321fdb852134ea4c7483fcd36a.
```

Reproduction:

```bash
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate5_round26_r1_f10_f13_frontier_verifier.py \
  --integrity-only

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate5_round26_r1_f10_f13_frontier_verifier.py \
  --replay

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate5_round26_r1_f10_f13_frontier_verifier.py \
  --self-test
```

Integrity and independent replay pass.  Hostile tests pass `81/81`.  Default
live mode exits `2`, preserving the fail-closed F10/F13, Gate-5 and CM2 status.
