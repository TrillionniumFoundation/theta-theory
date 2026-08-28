# CM2 one hundred fortieth direct assault

Date: 2026-07-24

Strict verdict: **the final Round139 positive-area fixed-`s=0` `R_1648`
rectangle now has a deterministic versioned adaptive path-cell identity, an
exact Round27-compatible path tuple, and a contained Round137-v1 basis-rank
upper-bound locator.  None is a historical maximal-component ID, historical
least rank, or Round35 restriction.**

## Final upstream anchor

The bridge now fails closed unless both final Round139 bytes agree:

```text
Round139 producer SHA256:     462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b
Round139 certificate SHA256:  64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0
Round139 result SHA256:       6e8f54c34154ea5ba3c95d4e901bc643c020a0a42e180241ae9053bb24f42236
```

The Round139 result is parsed from that certificate envelope.  Its producer
is hashed for provenance but is not imported or executed.

## Exact local identity advance

The current certificate supplies 1,648 closed positive-area collision rows.
Their ordered official-word IDs give:

```text
official sequence SHA256:  f504289edce554d47e17a90d7c886586a69f3ec4b64fafd90c718c50ca93221e
Round27 tuple SHA256:       5cec1061ec331e8f37929dfb1b2b2a78757309ba60198d571abd9e8cf6c70ed9
```

Together with the exact open `t,p` rectangle, fixed `s=0`, the final Round139
cylinder-row closure, the collision-row aggregate, and the explicit endpoint
policy, they determine:

```text
round140-fixed-s0-adaptive-path-cell:
a4a3be3cf7115abec08f372382ca7a863838e963a7d03af400d6a6ca58812b6a
```

This is the connected component of a one-cell finite adaptive registry.  Its
local registry rank is zero.  The four rational faces are artificial and
excluded.  Since every physical path predicate remains strict on the closed
rectangle, continuity extends the same regular path locally across each face.
The adaptive rectangle is therefore deliberately not claimed to be the
maximal connected component of the complete regular path fibre.

## Contained Round137-v1 upper bound

The independently normalized rectangle contains the lexicographically first
consecutive-grid box at denominator power 5883.  Its primitive Round137-v1
rank has:

```text
bit length:            23530
decimal digit count:    7084
decimal SHA256:        81ee4f795045d8478e621dbcaf2cba2437ccb168b34b770f995c012c0060927f
```

The corresponding witness-relative upper-bound locator is:

```text
round140-containing-component-upper-bound-locator:
7f62e720961a65aa52b737f9cb19a1df1d6f55d44aa89ef0a6f7b13c3fee12ac
```

The adaptive cell lies in one unique maximal connected component of the open
regular path fibre.  The separate set-theoretic locator for that containing
component is:

```text
round140-unique-containing-maximal-component-locator:
028dd77208582e33185707e1ea1ca31988e3cf4f698674fb8a0f791981dce90b
```

Both locators are witness-relative.  Neither is a historical
`c24-component` ID.  The displayed basis rank proves only that the
Round137-v1 least rank of the containing component is no larger; it does not
compute that least rank and does not retroactively instantiate Round27's
unnamed historical enumeration.

## Independent assault

The verifier does not import or execute either producer.  It independently
rebuilds the complete expected Round140 result from byte-pinned historical
contracts and the final Round139 certificate.

```text
formal verification:                 PASS
re-signed semantic mutations:       62/62 rejected
strict-JSON attacks:                18/18 rejected
in-process hostile paths:           20/20 rejected
dual producer hash seeds:           byte-identical
dual verifier hash seeds:           byte-identical
process hostile certificate inputs:  5/5 rejected
process hostile output targets:       7/7 rejected
```

The mutation suite explicitly attacks tuple and identity digests, source
provenance, fixed-`s` geometry, endpoint ownership, adaptive/maximal
substitution, contained-box minimality, v1 rank metadata, least-rank
invention, historical component-ID invention, every Round35 substitution
flag, owner/token/output counts, Gate5 maturity, and CM2 status.

## Exact remaining blocker

The historical route still requires all of:

1. a certificate for the maximal connected component `U` of the complete
   regular fixed-`s=0`, depth-1648 Round27 path fibre;
2. an executable crosswalk to the historical Round27 dyadic-basis
   enumeration, not merely the prospective Round137-v1 contract;
3. positive membership for a closure-contained basis box and a complete
   negative oracle excluding every earlier historical basis rank.

The available interval replay is a positive membership oracle.  Failure of
interval replay is inconclusive, and no complete outer boundary atlas exists,
so it cannot establish the negative half of a least-rank proof.

Consequently the final state remains:

```text
new deterministic adaptive path cells:        1
new exact nonempty Round27 path instances:     1
new Round137-v1 upper-bound locators:           1
historical Round27 component IDs/ranks:         0
Round35 restrictions:                          0
Round50 owners / Round54 tokens:                0
Round67 Omega_j records / q_j outputs:          0
global complete 18-field blocks:                0
Gate5 global maturity:                      10/18
Gate5:                               NOT_CERTIFIED
CM2:                              NO-GO_FOR_CLAIM
```
