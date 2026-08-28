# CM2 Round 137 — seed-independent dyadic basis/rank contract

Date: 2026-07-24

Round 137 freezes a new prospective executable enumeration of rational-dyadic
basis boxes.  It supplies the coordinate normalization and rank/unrank
algorithm that the historical Round27 and Round35 artifacts left
nonconstructive.  It does not claim that the new numeric ranks equal the
unnamed historical ranks.

## Exact affine normalization

All 24 frozen physical source cores are independently reconstructed from the
byte-pinned core registry.  For a core

```text
(t,p) in (t0,t1) x (p0,p1)
```

the exact increasing map is

```text
u = (t-t0)/(t1-t0)
v = (p-p0)/(p1-p0),
```

with inverse

```text
t = t0 + u(t1-t0)
p = p0 + v(p1-p0).
```

Thus every open core maps exactly and orientation-preservingly to `(0,1)^2`.
The 24 normalization rows have aggregate SHA256
`5a4d0cb4584cff86583c58ca21061574432a726e0a1ea67d0f7b9718ebfebd1f`.

## Prospective dyadic enumeration v1

At level `m>=2`, let

```text
I_m = binom(2^m-1,2).
```

A two-dimensional row is

```text
(m,a0,a1,b0,b1)
```

with all endpoints strictly interior and ordered.  The common denominator
`2^m` is minimal exactly when the four endpoint numerators are not all even.
This is one common-denominator rule; it does not require each coordinate pair
to be primitive separately.

The primitive level counts and zero-based offsets are

```text
2D count  = I_m^2 - I_(m-1)^2
2D offset = I_(m-1)^2

1D count  = I_m - I_(m-1)
1D offset = I_(m-1).
```

Rows are lexicographic within a level after all-even rows are skipped.  Exact
integer rank and unrank functions are frozen for both dimensions.

Independent exhaustive replay through level four gives:

```text
level     I_m     primitive 1D     primitive 2D
  2         3          3                  9
  3        21         18                432
  4       105         84              10584

total                 105              11025
```

All rank/unrank roundtrips, global-rank uniqueness, cross-level rational-box
uniqueness, offsets, and telescoping counts are exact.  Three large 1D and
three large 2D fixtures, through level 257, also roundtrip exactly.

## Round136 contained witness

The Round136 positive-area `R_1056` source box in physical core 14 is mapped
to normalized `(u,v)` coordinates.  Independent exact grid search finds the
first level with two strict consecutive grid points in each coordinate:

```text
minimal level m = 3809.
```

The resulting closed primitive dyadic box lies strictly inside the Round136
source box.  Its v1 rank has:

```text
bit length:             15234
decimal digit count:     4586
SHA256(decimal):
c6f579730386b27b3ccedc3c4159be4a8f42dfbcedceef52004d3a8b0a99fd4b
```

This rank is an upper bound for the connected component containing the
Round136 witness.  It is not the least component rank, because earlier basis
boxes have not been excluded.  The associated
`round137-component-witness-locator` is explicitly noncanonical and does not
deduplicate components.

## Independent verification

The verifier does not import or execute the Round137 producer.  It independently
reconstructs:

- all 24 affine normalization rows and their hashes;
- the common-denominator primitive rule;
- `I_m` counts and level offsets;
- independent 1D and 2D rank/unrank implementations;
- all 11130 exhaustive small rows;
- all six large fixtures;
- the minimal level-3809 Round136 witness;
- the 4586-digit upper-bound rank and its decimal hash;
- every historical and global nonpromotion field.

Formal verification is `PASS`.  It rejects:

```text
re-signed semantic mutations: 62/62
strict-JSON attacks:          22/22
path-safety attacks:          20/20
```

Strict-JSON coverage includes duplicate keys, floats, non-finite constants,
oversized JSON integers, malformed Unicode, trailing documents, and overlong
public decimal/hexadecimal rank strings.  The verifier bounds certificate
bytes and JSON integer digits before parsing attacker-controlled values.

## Strict boundary

The following remain null or zero:

```text
historical Round27 canonical rank / c24-component ID
Round35 source rank / r coordinate / image rank / restriction ID
Round50 owner keys
Round54 tokens
Round67 q_j outputs
global complete 18-field blocks
```

Consequently Gate5 remains `10/18` and `NOT_CERTIFIED`; CM2 remains
`NO-GO_FOR_CLAIM`.
