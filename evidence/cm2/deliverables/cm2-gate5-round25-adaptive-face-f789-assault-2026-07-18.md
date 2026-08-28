# CM2 Gate 5 — Round-25 adaptive-face F7--F9 companion leaf

Date: 2026-07-18  
Status: append-only strict leaf; no aggregate or recursive root modified

## Frozen conclusion

The 4,216 strict full-dimensional `RETURN_AT_1_INNER` boxes from the frozen
24-core adaptive frontier now receive three independent candidate-local
Gate-5 slots:

```text
F7  one_step_cut_growth_Z_sum       4,216 slots
F8  face_transversality_lower       4,216 slots
F9  face_C2_atlas_bound             4,216 slots
                                     ------------
                                     12,648 slots
```

The immutable slot rows, slot IDs, atom IDs and three-field packets are all
replayed in full and frozen by separate SHA-256 digests.  The compact
manifest retains representative rows rather than duplicating all 12,648
rows.

After an exact companion join to the separately audited round-25 F1--F6
candidate leaf, the local status on each of these 4,216 R1 atoms is `9/18`.
This is deliberately not global Gate-5 credit: the global maturity remains
`4/18`, complete 18-field blocks remain zero, and Gate 5 remains
`NOT_CERTIFIED`.

## 1. Why an adaptive rectangle costs only one F7 interval

Fix a parameter fibre `s` and one strict R1 adaptive atom `A`.  Its source
domain is a rectangle

```text
A_s = [t_0,t_1] x [p_0,p_1]
```

inside one of the already certified compact C24 cores.  On either canonical
unstable graph chart, the frozen characteristic theorem gives monotonicity
of `t` in boundary arclength and strict monotonicity of
`p=sin(phi)`.  Therefore the inverse images of both coordinate intervals
are intervals and their intersection is empty or one interval.  Thus a
canonical curve meets one adaptive atom in at most one component and pays at
most two artificial endpoints.

The invariant conditional density ratio is `2000/1999`, so the exact
unnormalised restriction estimate is

```text
Z_*(1_A F) <= (2000/1999) Z_*(F).                  (1.1)
```

Combining (1.1) with the already certified physical one-step coefficient
gives

```text
(2000/1999)*(360134800/360493663)
  = 720269600000/720626832337
  = 1 - 357232337/720626832337 < 1.               (1.2)
```

Equations (1.1)--(1.2) are per-atom, unnormalised statements.  This leaf does
not sum the cost of the union of 4,216 atoms and does not condition on an
atom whose mass may be arbitrarily small.

The two apparent extra boundary types do not add a phase cut:

- the `s` guard faces are inactive after fixing `s`;
- the destination-core predicate was admitted by a strict whole-closed-box
  Arb enclosure, so its preimage boundary does not meet the atom.

Consequently the previous draft's unpriced destination-preimage face is
removed rather than charged.

## 2. F8: a uniform strict face angle

At fixed `s`, the four phase faces are exactly two `r=constant` and two
`phi=constant` coordinate lines in Birkhoff coordinates.  Write the unit
unstable tangent as

```text
u = (1,V)/sqrt(1+V^2),
25/9 < V=dphi/dr < 29.
```

For a vertical coordinate face with unit tangent `e_phi`,

```text
|u wedge e_phi| = 1/sqrt(1+V^2)
                 > 1/sqrt(842) > 1/30.
```

For a horizontal coordinate face with unit tangent `e_r`,

```text
|u wedge e_r| = V/sqrt(1+V^2)
               > 1/sqrt(2) > 1/30.
```

Hence every one of the four actual fixed-fibre faces receives the common
strict transversality lower bound `1/30`.

## 3. F9: exact affine face atlases

Each individual face uses its unit-speed Birkhoff coordinate-line chart.
These charts are affine, so their coordinate `C2` seminorm is exactly zero:

```text
common individual-face C2 seminorm upper = 0.       (3.1)
```

Corners are codimension-two endpoints, not additional `C2` faces.  The leaf
does not claim the still missing global coincident-face/flux assembly; that
is part of F10 and the downstream flux-face operator fields.

## 4. Frozen unresolved-outer split plan

The finite adaptive cover still contains

```text
26,876 UNRESOLVED_OUTER parents,
base mass 44519/256000000,
depth histogram {12: 6816, 15: 20060}.
```

This leaf materializes one deterministic next split record for every parent.
The policy bisects the largest parent-normalised side, with tie order
`t,p,s`.  All present unresolved depths are multiples of three, so the next
scheduled axis is `t` on all 26,876 rows.  The plan therefore contains

```text
26,876 parent split records -> 53,752 child boxes,
child mass sum             = 44519/256000000 exactly.
```

Every split is prefix-free modulo shared owned faces and exactly mass
conservative.  A midpoint may propose more refinement, but every child must
be freshly classified by the whole-box 384-bit Arb trichotomy.  This leaf
does not assign any of the 53,752 children to R1 or Q1.

The recursive policy is fair: on an infinite unresolved lineage, the
normalised `t`, `p` and `s` diameters all tend to zero.  What remains open is
a certified finite-depth exhaustion or a quantitative outer-mass decay
rate.  Neither is inferred merely from fairness.

## 5. Strict next executable leaf

The next independent producer can consume the frozen 26,876-row split plan
without changing any earlier artifact:

1. reconstruct and replay all 53,752 child boxes at 384-bit Arb;
2. emit strict `RETURN_AT_1_INNER`, `SURVIVE_THROUGH_1_INNER` and residual
   `UNRESOLVED_OUTER` child rows with complete separation witnesses;
3. prove exact child-to-parent mass conservation and prefix-free ownership;
4. retain only residual rows in the next frontier, then schedule the `p`
   split and later the `s` split under the same normalised policy;
5. separately add a boundary-tube/local-diffeomorphism estimate if a
   numerical unresolved-mass rate is desired.

Only after the finite or summable outer cover is controlled should the same
machinery be iterated on Q1 survivors to form physical `R_n/Q_n` branches.
Those later rows must also carry numeric mass, unstable Jacobian/distortion,
common forward/reverse restriction IDs and the strong `q_n` load; none is
created by this face leaf.

## 6. Exact nonpromotion boundary

```text
R1-ATOM F7 CANDIDATE-LOCAL SLOTS:                 4,216 CERTIFIED
R1-ATOM F8 CANDIDATE-LOCAL SLOTS:                 4,216 CERTIFIED
R1-ATOM F9 CANDIDATE-LOCAL SLOTS:                 4,216 CERTIFIED
R1 LOCAL MATURITY AFTER EXACT F1--F6 JOIN:          9/18

F7 FOR UNION OF ALL 4,216 ATOMS:                  NOT CERTIFIED
NORMALIZED CONDITIONED Z UNIFORM IN ATOM MASS:    NOT CERTIFIED
GLOBAL COINCIDENT-FACE/FLUX ASSEMBLY:             NOT CERTIFIED
F10--F18:                                         NOT CERTIFIED
FINITE UNRESOLVED-OUTER EXHAUSTION:               NOT CERTIFIED
COMPLETE FINITE RAW R1/Q1 LEDGER:                 NOT MATERIALIZED
ARBITRARY-n PHYSICAL R_n/Q_n PARTITION:           NOT CERTIFIED
COMPLETE 18-FIELD R1 BLOCKS:                      0
GLOBAL GATE-5 MATURITY:                            4/18 UNCHANGED
GATE 5:                                           NOT CERTIFIED
CM2:                                              NO-GO FOR CLAIM
```

## 7. Frozen artifacts and replay

- `cm2_gate5_round25_adaptive_face_f789_cert.py`
- `cm2_gate5_round25_adaptive_face_f789_verifier.py`
- `cm2-gate5-round25-adaptive-face-f789-manifest-2026-07-18.json`
- `cm2-gate5-round25-adaptive-face-f789-manifest-2026-07-18.sha256`

```bash
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate5_round25_adaptive_face_f789_verifier.py \
  --integrity-only

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate5_round25_adaptive_face_f789_verifier.py \
  --replay

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate5_round25_adaptive_face_f789_verifier.py \
  --self-test
```

The hostile suite passes `91/91`.  Default live mode exits `2`, preserving
the fail-closed Gate-5 and CM2 status.
