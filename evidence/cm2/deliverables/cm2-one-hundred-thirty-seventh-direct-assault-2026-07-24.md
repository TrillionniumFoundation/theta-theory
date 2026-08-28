# CM2 one hundred thirty-seventh direct assault

Date: 2026-07-24

Strict verdict: **a prospective seed-independent dyadic basis enumeration and
exact rank/unrank contract is now executable and independently verified.  It
does not recover historical Round27/35 numeric labels and does not create an
owner, q_j output, Gate5 block, or CM2 theorem.**

## Closed advance

Round27 and Round35 used countability through unnamed dyadic enumerations.
Round137 now freezes, for future work:

- an exact increasing affine map from each of 24 physical core rectangles to
  `(0,1)^2`;
- a common-denominator primitive rule;
- exact 1D and 2D level counts and offsets;
- zero-based lexicographic rank and unrank functions;
- exhaustive small-level and large-index fixtures.

At level `m`, the two-dimensional primitive count is
`I_m^2-I_(m-1)^2` and its offset is `I_(m-1)^2`; the one-dimensional analogues
are `I_m-I_(m-1)` and `I_(m-1)`.

## Round136 witness

The positive-area Round136 `R_1056` box contains a closed primitive dyadic
basis box at the first possible consecutive-grid level `m=3809`.  Its new-v1
rank has 4586 decimal digits with SHA256
`c6f579730386b27b3ccedc3c4159be4a8f42dfbcedceef52004d3a8b0a99fd4b`.

This proves a finite v1 rank upper bound for the component containing the
witness.  It does not prove least rank and cannot be renamed as the historical
canonical component rank or a `c24-component` ID.

## Independent security verification

The verifier is source-independent from the producer and reconstructs the
entire certificate result.  Formal status is `PASS`:

```text
semantic re-sign mutations rejected: 62/62
strict-JSON attacks rejected:        22/22
path-safety attacks rejected:        20/20
dual hash-seed artifacts:            byte-identical
missing/tampered certificates:       rc=1, no output
```

Public 4586-digit decimal and corresponding hexadecimal fields are
length-, syntax-, hash-, and metadata-checked without first converting
attacker-controlled strings to unbounded integers.

## Frozen global state

```text
historical Round27 component rank / ID: null
Round35 restriction fields:            null
Round50 owner count:                       0
Round67 q_j count:                         0
global complete 18-field blocks:           0
Gate5 global maturity:                 10/18
Gate5:                          NOT_CERTIFIED
CM2:                         NO-GO_FOR_CLAIM
```

The next honest use of this contract may enumerate new-v1 basis witnesses or
derive prospective component locators.  It must not retroactively assign
historical identifiers without a separately frozen crosswalk and least-rank
proof.
