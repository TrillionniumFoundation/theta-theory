# CM2 Gate 4: same-occurrence weak-Borel operator/test payload frontier

Date: 2026-07-16  
Verdict: **Gate 4 remains `NOT_CERTIFIED`**.

This pass joins the frozen same-occurrence product recovery kernel to the
already certified finite-signed-measure/bounded-Borel-test operator layer.  It
closes one missing ledger entry, but only at the weak Borel level.  No strong
CM2 norm is inferred from total variation.

## 1. Frozen inputs and scope

The certificate binds, by SHA-256:

- the query-independent product record
  `(e,s,K,j,owner,polarity,restriction)` and its numerical joint recovery
  moment;
- the physical prefix/suffix contractions on
  `M_b` (finite signed Borel measures with TV norm) and
  `B_b` (bounded Borel tests with sup norm);
- the corrected 64-row, 128-coordinate occurrence/Kac ledger; and
- the frozen v52 contract.

The product record is uniform for `|s|<=1/400`.  The corrected physical event
current is the frozen 64-row current.  Its actual Borel Kac output and the
finite-`s` product-record envelope are kept as distinct claims: the latter is
not promoted to a finite-`s` physical current or `MT_DQ` identity.

## 2. Weak Borel source/test ledger

For a deterministic physical prefix or suffix `F`,

```text
||F_* nu||_TV <= ||nu||_TV,
||g o F||_infty <= ||g||_infty.
```

On the disjoint return partition these bounds retain constant one, because
the TV masses of the restrictions add exactly.  The same record, restriction,
owner and polarity are used by both orientations before a later bounded test
is selected.  Therefore every controlled product record has a
query-independent weak-Borel source/test payload.  The height-nine tower and
test sum have multiplier at most nine.

This proves:

```text
PRODUCT-RECORD WEAK-BOREL OPERATOR/TEST PAYLOAD: CERTIFIED.
```

It does not prove a regular-density, standard-family, dynamic-`C1`, or
flux-face bound.

## 3. Corrected current and Kac payload

On one corrected occurrence with positive law `m_e`, the hit-minus-miss
current satisfies

```text
||J_e||_TV <= 2 m_e.
```

The two singular Kac coordinates share that occurrence with marks `(+1,-1)`;
their direct-sum `l1(TV)` cost is at most `4 m_e`.  The worst height-nine lift
is consequently at most `36 m_e`.  Globally this replays exactly as

```text
event current TV                         <= 16128/5,
two singular coordinates in l1(TV)      <= 32256/5,
height-nine lifted pair in l1(TV)       <= 290304/5.
```

These are single-occurrence charges.  Forward and reverse views are
alternative views of the same record, not two additive occurrences.

## 4. Absorption into the controlled product envelope

The frozen product envelope is

```text
C_prod(s,a,K)
 = 2^K exp(gamma(R_fw+R_rev))
   max(204*2^B_s(a), C_mesh, 2),

gamma  = 1/12060,
C_mesh = 69986663973833932800.
```

The height-nine two-coordinate Borel payload has coefficient `36` per unit
base occurrence mass, while `C_mesh>36`.  Thus the existing maximum already
dominates the new payload; no new additive forward/reverse charge is needed.
The standalone clocked payload moment is strictly bounded by

```text
36 * (2*3^50) = 72*3^50
```

per unit base occurrence mass.  The previously certified integral bound for
`C_prod` therefore remains unchanged:

```text
1087598065258783059015245434544676138185728521412801591795461
----------------------------------------------------------------
                         6710886400000
```

before the fixed collision-flux normalizer `Z_N^-1`.

## 5. Exact non-promotion boundary

The join does **not** certify any of the following:

1. TV control of standard-family boundary `Z`;
2. TV control of regular-density variation;
3. `Linf` control of a dynamic-`C1` inverse test pullback;
4. a flux-face atlas or `FACE_TIME` bound;
5. finite-`s` Gate-3 physical current/common branch-record `MT_DQ` matching;
6. finite time-zero `Z` for the native countable partition;
7. arbitrary or unbounded repeated-indicator recovery;
8. the complete same-occurrence CM2 strong-operator ledger; or
9. complete `C_fw`, `C_rev`, final `q`, or Gate 4.

This distinction is structural, not a missing scalar factor: the frozen
countermodels have bounded TV while standard-family boundary or inverse
`C1` pullback cost diverges.

## 6. Reproduction

```bash
python -m py_compile \
  deliverables/cm2_gate4_product_borel_payload_frontier_cert.py \
  deliverables/cm2_gate4_product_borel_payload_frontier_verifier.py

python deliverables/cm2_gate4_product_borel_payload_frontier_cert.py
python deliverables/cm2_gate4_product_borel_payload_frontier_verifier.py --replay
python deliverables/cm2_gate4_product_borel_payload_frontier_verifier.py --integrity-only
python deliverables/cm2_gate4_product_borel_payload_frontier_verifier.py --self-test
python deliverables/cm2_gate4_product_borel_payload_frontier_verifier.py
```

The first four commands exit `0`; the final live command prints the
fail-closed boundary and exits `2`.  The verifier rejects 16/16 semantic or
integrity mutations.

## 7. Final verdict

```text
PRODUCT-RECORD WEAK-BOREL OPERATOR/TEST PAYLOAD: CERTIFIED
CORRECTED-CURRENT PHYSICAL BOREL KAC PAYLOAD:    CERTIFIED
FINITE-s PHYSICAL CURRENT / MT_DQ MATCH:         NOT_CERTIFIED
COMPLETE CM2 STRONG-OPERATOR LEDGER:              NOT_CERTIFIED
COMPLETE C_fw / C_rev / FINAL q:                  NOT_CERTIFIED
GATE 4:                                           NOT_CERTIFIED
```

The next honest Gate-4 step is no longer another weak scalar charge.  It is
the branchwise strong-space propagation ledger, synchronized with the
finite-`s` Gate-3 physical current/`MT_DQ`, followed by characteristic-boundary
control for the actual return-word restrictions.
