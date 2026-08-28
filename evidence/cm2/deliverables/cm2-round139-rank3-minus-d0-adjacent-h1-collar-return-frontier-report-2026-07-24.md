# CM2 Round 139 — minus-D0 adjacent H1 collar return frontier

Date: 2026-07-24

Round 139 certifies one exact half-open H1 graph collar immediately adjacent
to the Round 138 D3=0 event from the minus/BYPASS side. It also certifies a
positive-area fixed-s rectangle inside the collar enclosure. Both objects
have one fixed 1648-collision first-return word.

This is a local one-sided result. It does not materialize a global Round35
restriction or component, a Round50 owner, a Round54 token, or a Round67
`Omega_j`/`q_j` record.

## Deep D3=0 root and common leaf

The construction remains on the exact Round138 implicit slope-four leaf

```text
x = sqrt(17) r,
r = (4/25) asin(t),
v = asin(p) - 4r = b_star.
```

Five fixed-rounding Newton locator steps are followed by a proof bracket with
exact width `2^-18431`. Strict endpoint signs and strict positivity of `D_t`
on the whole bracket prove existence and uniqueness. The induced `b_star`
outer enclosure uses a fixed 16448-bit dyadic grid and is strictly nested in
the Round138 enclosure.

The frozen local parent identifier is

```text
round138-local-slope4-parent-W:
216354a2f6fa10bf6b674038aad2d5dc1f80ea0b4c97d973864d0dc03209412c
```

## Exact one-sided H1 collar

The certified graph collar is

```text
[x_star - 2^-5888, x_star).
```

The proof replays the closed branch-continuation enclosure through
`x_star`. Along the exact leaf, D3 is strictly increasing, is negative at the
far endpoint, and reaches zero only at `x_star`.

At collision 3 the candidate `W[0,0]` is exactly the D3 tangency at the
excluded endpoint. It is omitted only from that one closed-endpoint analytic
branch-continuation decision. The certificate does not claim that the
tangent endpoint is a regular billiard trajectory. Every nonanchor retained
and full-radius-four decision is strict on the entire closed enclosure.

## Positive-area fixed-s rectangle

Round139 also takes the first t-half of the collar rectangle and recomputes a
fresh exact-leaf p-hull. The resulting rational rectangle has

```text
t-width floor log2:  -5889
p-width floor log2:  -5890
area floor log2:    -11778
```

Its whole box has D3 strictly negative, with anchor-miss dyadic depth 5886.
The ordinary collision replay therefore includes the anchor; no analytic
endpoint exclusion is used for this positive-area object. This local
positive area is not an owner-law positive-mass conclusion.

## Complete first-return replays

| Object | Return depth | Retained histogram | Full tests | Terminal target |
|---|---:|---:|---:|---|
| exact half-open H1 graph collar | 1648 | `55:505, 57:1143` | 265,328 | `G[-7,-13]` |
| positive-area fixed-s rectangle | 1648 | `55:505, 57:1143` | 265,328 | `G[-7,-13]` |

The common destination core is

```text
core:e47f553e056452faa012129434cdbbb6a55cd9671a19ea04e6b8a9f43054c4c2
```

Across the two objects the certificate contains:

```text
collision rows:                       3296
strict preterminal nonreturns:         3294
strict terminal returns:                  2
full-radius-four candidate tests:    530656
official-word occurrences:             3296
```

Every collision is central and has incidence rank 14. Both objects have the
same owner and official-word sequences:

```text
owner sequence:
c50277af0c038521b8933672d2a5a2b9035473895694c3c2878842274337cac3

official-word sequence:
f504289edce554d47e17a90d7c886586a69f3ec4b64fafd90c718c50ca93221e

compact path:
c37571201fa15065a7f8e4eeec9df5a79f36e077feac37a1aec7b910970e1f17
```

Each sequence contains 141 distinct official-word keys.

## Local other-cut clearance

All nonanchor boundary decisions remain strict on the closed
length-`2^-5888` collar, including its far endpoint. Compactness and
continuity therefore give the local intrinsic statement

```text
d_other(x_star, minus branch) > 2^-5888.
```

The strict decision-value ledger has worst dyadic depth 18. Those
decision-value margins are not identified with H1 distance, and the local
H1 statement is not a global component-separation theorem.

## Independent verification

The verifier does not import or execute the Round139 producer. It rebuilds
the root, fixed dyadic enclosures, both objects, all 3296 collision rows,
retained and full-radius-four searches, official words, homogeneity labels,
incidence ranks, and C24 return decisions using the byte-pinned independent
Round138 verifier kernel.

Complete reconstructions at 24576 and 32768 bits are identical. Two process
invocations with distinct `PYTHONHASHSEED` values produce byte-identical
formal verification artifacts.

```text
formal verification:                  PASS
re-signed semantic mutations:        24/24 rejected
strict-JSON attacks:                 19/19 rejected
in-process path attacks:             13/13 rejected
process-level hostile I/O:           12/12 fail-closed
```

Frozen hashes:

```text
producer:            462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b
certificate:         64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0
certificate result:  6e8f54c34154ea5ba3c95d4e901bc643c020a0a42e180241ae9053bb24f42236
verifier:            cb96e0e1a74abcac4254f20584bab6997edb8de69f0d979f1d65d4c3fdfadd09
verification:        57093537ae3f464e276da830ee5821ffbe3576278c71adbe111b22a128f3005f
verification result: e96609b3ff1ba35c94e224c5d16897ed6d173fe69cc3cbf260ff85e5340165e1
```

## Strict global boundary

```text
local exact graph collars:               1
local positive-area return rectangles:   1
global Round35 restrictions:             0
global component ranks:                  0
global short cells / image recuts:   0 / 0
Round50 owners:                           0
Round54 t54 / pi54 maps:              0 / 0
Round67 Omega_j / q_j:                0 / 0
global complete 18-field blocks:          0
Gate5 global maturity:                10/18
Gate5:                         NOT_CERTIFIED
CM2:                        NO-GO_FOR_CLAIM
```
