# CM2 Round 134 — Round28 exact-seed occurrence-incidence frontier

Date: 2026-07-24

Round 134 closes the previously missing typed crosswalk from the 64
materialized Round132 occurrence records to the Round113 exact-seed target
geometry.  It then proves, on the entire frozen Round113 parent rectangle,
that none of the twelve compatible target lifts has a moving-occurrence
tangency root.

The 64 Round132 records split exactly into:

- 44 source-`G` compatible records;
- 20 source-`W` type mismatches;
- 16 unique signed target sheets;
- 12 unique target lifts.

Round122 did not itself type-join the Round28 occurrence IDs to these target
lifts.  Round134 installs that missing crosswalk and pins both its signed-sheet
and target-lift digests.

## Whole-rectangle main proof

The parent cell is
`round113-cell:08b7ca8449af5f6e8d4e3abce98803656664ed7ec957aba62406763b68b2fea6`.
The full parameter domain is

```text
c0 in [3/65536, 1/16384]
b3 in [1/32768, 1/16384]
s  in [-1/400, 1/400].
```

At 2048-bit precision, outward-rounded Arb interval arithmetic evaluates each
target discriminant on this whole product box, together with the certified
implicit-`t` root enclosure.  This is the main proof; it is not a finite
sample or a corner argument.

The twelve target lifts are

```text
W[-1,-1] W[-1,-2] W[-1,0] W[-1,1]
W[-2,-1] W[-2,0] W[0,-1] W[0,-2]
W[0,0]   W[0,1]   W[1,-1] W[1,0].
```

The whole-box enclosures give:

- 2 strictly positive discriminants, for `W[-1,-1]` and `W[-1,-2]`;
- 10 strictly negative discriminants;
- 0 zero discriminants and 0 tangency roots;
- a uniform strict absolute margin greater than `1/100`.

A positive discriminant means two transverse line intersections, not a
tangency root.  A negative discriminant means a whole-line miss.  Therefore
neither sign supplies the active transverse tangency root required by the
Round28 moving-occurrence construction.

The tightest enclosure is the still-negative `W[-1,0]` interval

```text
[-374189179/25000000000, -101296291/7812500000].
```

Every target row also carries eight corner evaluations whose signs agree with
the whole-box enclosure.  These corner values are auxiliary checks only and
are never used as the proof of the rectangle-wide statement.  The twelve-row
closure hash is
`5a5e25aa322a70b03cb895d4b8e7bd4056171af78fb8b81f0dda5e1c0193b21f`.

Hence the exact-seed Round28 moving-occurrence root count is zero and the
strict scoped status is `CERTIFIED_EMPTY`.

## Independent crosschecks

The verifier independently rebuilds the Round122 exact-seed empty ledger:

- 24 common-refinement children;
- 72 child-stage rows;
- stage candidate counts `57/55/57`;
- 169 candidates per child and 4056 checks in total;
- all seven physical boundary kinds checked;
- 0 physical faces and 0 residual physical faces.

This crosscheck remains restricted to one exact `b` seed and the common
collar `|s|<=2^-512`.

Round75 cannot fill the missing occurrence carrier.  Its 16 physical
components and 32 curves are stationary destination-core `t/p` boundary
preimage crosscuts, whereas Round28 requires a moving occurrence-pullback
family at an active transverse tangency root.  The substitution is rejected
as `REJECTED_TYPE_MISMATCH`.

## Frontier and verification

The exact-seed incidence result is not a global absence theorem.  Actual
nonempty `n>=2` occurrence-pullback incidence elsewhere remains
`UNKNOWN_NOT_CERTIFIED`.  The first unpaid construction is a genuine
fixed-`s`, `n>=2`, parent-`W` path component crossing a Round28 moving
occurrence graph, followed by enumeration of the complete primitive-free
active fibre.

The independent verifier neither imports nor executes the Round134 producer.
It independently rebuilds the 64-record crosswalk, evaluates all twelve
whole-box discriminants, recounts the Round122 ledger, and rejects 69
re-signed semantic mutations and 18 strict-JSON attacks.

No new occurrence component, rank-zero component, complete active primitive
fibre, owner key, recordwise `q_j` output, owned `Omega_j` record or global
18-field block is materialized.

Global safety is unchanged:

- Gate5 global maturity: `10/18`;
- global complete 18-field blocks: `0`;
- Gate5: `NOT_CERTIFIED`;
- CM2: `NO-GO_FOR_CLAIM`.
