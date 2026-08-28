# CM2 Round 135 — wide positive-Borel local robustness

Date: 2026-07-24

Round 135 widens the Round129/130 exact-fibre construction from the tiny
half-width `2^-512` collar to the closed interval

```text
lambda in [5/131072, 7/131072],
center  = 3/65536,
half-width = 2^-17.
```

This remains a local theorem in one frozen Round113 parent and one Round117
operator cell. It is not global return-word or all-Borel coverage.

## Sharp frozen-cell boundary

The new collar lies strictly inside

```text
[1/32768, 1/16384].
```

Among negative powers of two, `2^-17` is the largest centered half-width with
strict containment. The next half-width, `2^-16`, gives exactly

```text
[1/32768, 1/16384],
```

so both strict parent-cell inequalities become equalities. Round 135 therefore
records `2^-16` as the first frozen-cell obstruction rather than silently
crossing an operator-cell boundary.

The implicit root graph is monotone on the whole collar: `F_t<0`,
`F_lambda>0`, `dt/dlambda>0`, and

```text
1/3000000 < db/dlambda < 1/1500000.
```

Consequently the `b` image is a nondegenerate positive-Borel interval with
certified length greater than `1/196608000000`.

## Dependency-preserving recut construction

Direct subtraction of adapted endpoints is unstable at the `10^-90` scale.
Round 135 instead certifies the positive normalized derivatives

```text
D1 = -partial_x(a1)/delta
D2 =  partial_x(a2)/delta
D3 = -partial_x(a3)/delta
Vi(lambda,x) = integral_0^x Di(lambda,y) dy
```

on 64 source-`x` cells. Lower and upper Riemann envelopes are then inverted
monotonically. The terminal integral enclosures satisfy

```text
6   < V1(1) < 7
17  < V2(1) < 18
192 < V3(1) < 193.
```

This materializes:

- 192 normalized derivative cells;
- 23 input recut-root guards;
- 192 stage-three recut-root guards;
- 24 common-refinement children;
- 215 merged interior cuts;
- 216 positive stage-three output fragments.

All guard orders are strict. Every common child has positive source length,
and every stage-three fragment has normalized output length strictly greater
than `4/125`.

## Complete physical and F17 replays

The full collar is split into four closed root-graph subcollars. The complete
Round122 typed physical audit is replayed on each:

```text
candidate checks per subcollar:  4056
candidate checks in total:      16224
physical five-face incidences:      0
residual physical faces:            0
physical F10:                        0
```

The four closed boxes cover the full collar and replay shared endpoints in
both adjacent boxes. A coarser two-slice interval remains dependency-unresolved
at `W[-1,-2]`; it is explicitly recorded as an interval diagnostic, not a
mathematical incidence.

All 72 graph-current guards (`24 children × 3 stages`) are independently
replayed. Their actual generator bounds remain strictly below `8`, `2`, and
`0` by stage, with stage two identically zero. The authoritative dynamic F17
bounds remain

```text
4915200 / 2457600 / 2457600.
```

## Local transport and cemetery boundary

Eighteen transport rows specify new wide-family object-ID constructors using
the family root and canonical exact-`lambda` key. They are finite family
templates, not an enumeration of uncountably many actual fibre slots.

For every exact fibre in this collar, the local census remains:

```text
input recuts:                       26
common children:                    24
base keys:                         120
field slots:                      2160
local complete level blocks:       120
local complete child packets:       24
local field maturity:             18/18
```

The half-open output partitions are exhaustive, so the restricted relative
cemetery is zero. This is separate from the physical-F10 emptiness statement.
Neither supplies ambient pre-regularization cemetery, all-time owner
cemetery, positive cemetery payment, global raw-Z/Orlicz recovery, or owner
drift.

## Evidence and independent verification

The frozen certificate contains exactly 970 independently closed evidence
rows:

```text
5 + 9 + 192 + 23 + 192 + 24 + 215 + 216 + 4 + 72 + 18 = 970.
```

The verifier does not import or execute the Round135 producer. It reconstructs
the complete result and all 970 rows from byte-pinned upstream inputs, checks
all row and group hashes, and confirms 970 unique primary evidence IDs.

Formal verification is `PASS`. It rejects all 59 re-signed semantic mutations
and all 18 strict-JSON attacks. Dual `PYTHONHASHSEED` cold replays are
byte-identical to the formal verification artifact. Missing, tampered,
symlink, hardlink, FIFO, aliasing, and protected-output cases all fail closed.

## Strict global state

```text
wide local every-exact-fibre maturity:  18/18
physical F10:                               0
global complete 18-field blocks:            0
Gate5 global maturity:                  10/18
Gate5:                           NOT_CERTIFIED
CM2:                          NO-GO_FOR_CLAIM
```

