# CM2 Gate 5 round 39: moving-occurrence F10 physical L3/2 moment

Date: 2026-07-19  
Status: **all 64 moving-occurrence F10 seeds and 128 oriented traces now have
an explicit physical raw-coarea `L^(3/2)` bound; arbitrary-`R_n` and all-face
F10 remain open**

## 1. Physical endpoint-rank moment

On the positive unnormalized endpoint coarea measure, the frozen rank
theorem gives

```text
mass < 8064/5,
m{B>b} <= (9158592/6875) 4^(-b),  b>=14.
```

Set `a=2^(3/2)`.  The integer layer-cake identity is

```text
a^B=a^14+(a-1) sum_{b=14}^{B-1} a^b.
```

Using the safe exact bounds

```text
a^14=2^21,
a-1<2,
sum_{b>=14}(a/4)^b < 7/256,
```

gives the explicit physical moment

```text
integral 2^(3B/2) dm
 < (8064/5)2^21 + (7/128)(9158592/6875)
 = 46506443753721/13750.
```

This is measured directly on the face/coarea object used by the moving-face
F10 field.  It is not retyped as fixed-`s` collision-SRB mass.

## 2. Same-ID F10 envelopes

Round 33 joins the 64 moving occurrence IDs to the same endpoint rank and
certifies

```text
rho <= 18/5,
|d_theta rho_rev| < (4374/125)2^B,
|d_theta rho_fw | < (8424/125)2^B.
```

For every integer `B>=14`, the raw seed coarea-regularity costs satisfy

```text
N_rev < 35*2^B,
N_fw  < 68*2^B.
```

Since `35^(3/2)<35^2` and `68^(3/2)<68^2`, the physical bidirectional bounds
are

```text
integral N_rev^(3/2) dm < 2278815743932329/550,
integral N_fw ^(3/2) dm < 107522897958602952/6875.
```

Thus all 64 seeds and all 128 oriented traces have certified physical
raw-coarea `L^(3/2)` F10 moments.

## 3. Round-38 exponent criterion is met on this subatlas

With endpoint scale `eta` and

```text
B=max(14,ceil(log2(1/eta))),
```

the tail `4^(-B)` gives physical margin exponent `alpha=2`, while the F10
envelopes proportional to `2^B` give blow-up exponent `r=1`.  Taking
`p=3/2`,

```text
r*p = 3/2 < 2 = alpha.
```

This is the first positive physical realization of the Round-38 criterion
for a nonzero moving F10 subatlas.  It removes the earlier uncertainty about
`r/alpha` for these seed faces only.

## 4. Strict boundary

```text
MOVING-OCCURRENCE SEED F10 L3/2:       CERTIFIED (64 / 128)
FIXED-s COLLISION-SRB MASS MOMENT:      NOT ASSERTED
ARBITRARY-R_n PULLBACK F10:             NOT CERTIFIED
COMPLETE ALL-FACE F10:                  NOT CERTIFIED
F12 / F13 / STRONG CEMETERY:            NOT CERTIFIED
F14--F18 / COMPLETE BLOCKS:             NOT CERTIFIED / 0
GATE-5 MATURITY:                        7/18 UNCHANGED
CM2:                                    NO-GO
```

The next F10 task is to transport this same-ID seed estimate through every
finite-rank pullback occurrence and combine it with the already certified
all-face F9 path registry.  Owner/singularity and core-preimage F10 classes
still need their own physical margin exponents.

## Evidence

- `deliverables/cm2_gate5_round39_moving_occurrence_f10_l3over2_cert.py`
- `deliverables/cm2_gate5_round39_moving_occurrence_f10_l3over2_verifier.py`
- `deliverables/cm2-gate5-round39-moving-occurrence-f10-l3over2-manifest-2026-07-19.json`

Syntax, frozen dependency hashes, strict JSON, exact rational replay and
live fail-close pass.  The verifier rejects `23/23` hostile mutations.
