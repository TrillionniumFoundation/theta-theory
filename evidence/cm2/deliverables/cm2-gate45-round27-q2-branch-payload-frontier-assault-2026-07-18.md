# CM2 Gate 4/5 round-27 Q2 branch-payload frontier

Verdict: **114,006 strict Q2-inner atoms now carry exact typed mass formulas,
one common forward/reverse restriction ID, invariant-area Jacobian 1 and one
symbolic once-charged q2 record; numerical unstable payload, F14--F18,
weighted tails and CM2 remain NOT CERTIFIED.**

## 1. Scope

This append-only leaf starts from the frozen round-26 time-two registry.  It
does not reuse representative points.  The producer reruns the complete
384-bit Arb recursion on all 2,868 Q1 parents, reconstructs the 416,994
depth-at-most-16 leaves and selects exactly the 114,006
`SURVIVE_THROUGH_2_INNER` atoms.

Every selected atom has a strict unique collision owner at time two and is
strictly outside the full 24-core union at both times one and two.  The
round-26 zero admitted R2 count is always qualified by the finite depth-16
cover; it is not interpreted as physical R2 emptiness.

## 2. Exact mass ledger

Each Q2 atom receives a unique mass slot containing four separately typed
objects.

1. Its rational coordinate-base contribution
   `R_source * dt * dp`, averaged over the full parameter window.
2. Its exact fixed-fibre unnormalised collision-area mass
   `R_source * dp * (asin(t1)-asin(t0))`.
3. The same exact mass multiplied by the atom's parameter-guard fraction.
4. The corresponding exact normalised collision-SRB formula, with the
   normalising factor `4*pi*(R_G+R_W)` left explicit.

The rational coordinate-base total is exactly

```text
5257799/5120000000.
```

It is not renamed an exact collision-SRB mass.  On every positive-width atom,
the physical collision-area mass is strictly between the coordinate-base
mass and `1401/1000` times that mass.  The complete per-atom formula ledger is
committed by a streaming SHA-256 digest.

## 3. One physical restriction, two nonadditive views

For each atom the source core, the strict time-one target and the strict
time-two target define one immutable two-collision word.  The source box,
parent ID, refinement suffix, clock and word generate one
`restriction:q2:*` ID.  The forward view is `T_s^2|A_atom,s`; the reverse view
is its inverse on `B_atom,s=T_s^2(A_atom,s)`.  Both views reference the same
restriction ID and the same exact mass slot, so they are not charged twice.

These are genuine fixed-fibre Borel/smooth restriction IDs.  They are not
common strong recovery carriers: no standard-family/flux/dynamic-test carrier
atlas has yet been joined to them.

## 4. Three Jacobians are kept distinct

The collision map preserves Birkhoff area `dr dp`.  Hence every regular
collision has invariant-area Jacobian 1, and every certified two-collision Q2
word has composed invariant-area Jacobian 1.

Neither of the following is inferred:

- the adaptive `(t,p)` coordinate Jacobian equals one;
- the one-dimensional unstable Jacobian equals one.

The existing universal unstable estimate is therefore installed only as a
conditional template.  After physical homogeneity refinement at both steps
and a canonical recut before each collision,

```text
two-step adapted inverse unstable Jacobian <
(144000/180337)^2 = 20736000000/32521433569,

two-step canonical-recut log-variation <
2*(3/200000) = 3/100000.
```

The round-26 Q2 rows carry neither time-one nor time-two homogeneity-child
IDs, nor canonical-recut component IDs.  Consequently these bounds are not
F5/F6 slots on the unsplit atoms.  The first missing strong-schema field is
F2, `physical_homogeneity_subbranch_table`.

## 5. q2 and F14--F18

Every restriction receives one symbolic charge record

```text
q2_atom=max(C_fw(atom),C_rev(atom),2)*m2_atom.
```

It is tied to the same restriction ID and exact mass used by both views.
However, numerical common-carrier `C_fw` and `C_rev` are absent, so numerical
`q2` count remains zero and no q-weighted sum or tail is asserted.

The downstream operator fields remain empty:

| field | materialised Q2 slots | first missing interface |
|---|---:|---|
| F14 regular-density cost | 0 | physical homogeneity rows and F10 |
| F15 standard-family cost | 0 | Q2 characteristic F7 and survivor recovery |
| F16 flux-face cost | 0 | physical moving face/coarea/DQ atlas |
| F17 dynamic-test cost | 0 | physical DQ current and numerical common-carrier costs |
| F18 operator phase block | 0 | F14--F17 are not assembled |

Thus neither a strong-q weighted tail nor an induced strong Lasota--Yorke
coefficient follows from this leaf.

## 6. Verification

The fail-closed verifier checks frozen dependency hashes, exact schemas,
rational composition arithmetic, all nonpromotion boundaries, and 82 hostile
mutations.  Its `--replay` mode reruns the full round-26 384-bit Arb cover and
reconstructs the complete Q2 branch-payload digest.  Live mode exits `2` by
design because the claimed CM2 conclusion remains unavailable.

Final frozen verification counts and SHA values are recorded in the leaf
manifest and SHA-256 chain.

## 7. Strict status

```text
Q2 exact typed mass slots:                 114006 CERTIFIED
Q2 common fw/rev Borel/smooth IDs:         114006 CERTIFIED
Q2 composed collision-area Jacobian 1:     114006 CERTIFIED
Q2 symbolic once-charged q2 records:       114006 CERTIFIED
Q2 numerical unstable Jacobian/distortion: NOT CERTIFIED
Q2 numerical strong q2:                    NOT CERTIFIED
Q2 F14--F18:                               0 / NOT CERTIFIED
arbitrary-n Rn/Qn:                         NOT CERTIFIED
Gate 4 / Gate 5 / CM2:                     NOT CERTIFIED / NO-GO
```
