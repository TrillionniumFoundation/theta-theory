# CM2 Round162 exterior frozen-prefix pruning block

Date: 2026-07-25

## Decision

One strict `EARLIEST_PREFIX_EXCLUDED` block is certified for the pinned
Round139 return signature.  It is not a full exterior-sheet exclusion and
does not close D02.

Round139's first collision has owner `W[1,0]` and outgoing chart W.  The
exact Gate3 target reduction was rebuilt over all 162 horizon lifts using
rational arithmetic.  On source chart `W:W`, target `W[1,0]` satisfies

```text
empty_outgoing_halfspace
support_upper=-707/1000 < R_source-R_target=0.
```

It is therefore absent from the complete 55-target conservative registry on
that chart.  Before any root-order decision, the required first owner is
impossible.  The open `W:W` cell is consequently excluded for this one
frozen prefix.

## Exact census and two scopes

The pinned four-chart source-W census was independently summed:

```text
all source-W leaves      76,828
unique-first             26,204
tangency-graph               56
multi-candidate          50,568
```

For the pinned frozen prefix, all 18,930 `W:W` leaves are excluded:

```text
W:W unique-first          6,518
W:W tangency-graph           24
W:W multi-candidate      12,388
```

The remaining frozen-prefix work outside `W:W` is therefore:

```text
remaining leaves         57,898
unique-first             19,686
tangency-graph               32
multi-candidate          38,180
```

The 6,518 `W:W` unique leaves are the present immediate unique-first
short-circuit credit.  The 24 `W:W` tangency cells and 12,388 multi cells
remain relevant to chart-boundary gluing or other return signatures.  Thus
the all-signature queue still contains all 56 source-W tangencies and all
50,568 source-W multi-candidate cells.

An additional full 192-bit cold reconstruction of the two representative
atlases found owner `W[1,0]` on 886 `W:E` unique leaves, 155 `W:N` leaves,
155 reflected `W:S` leaves, and zero `W:W` leaves.  This implies a potential
25,008/26,204 owner-mismatch short circuit.  That stronger count is reported
only as a replay observation and is not claimed by the fast certificate;
the remaining 1,196 target-matching unique leaves still require an outgoing
chart check.

## Verification

The verifier does not import or execute the producer.  It independently:

1. pins the Gate3 atlas, Gate3 first-hit registry, their two source files,
   and the Round139 certificate/source;
2. reconstructs the Round139 first owner/outgoing-chart prefix from both
   the one-dimensional and positive-area collision rows;
3. rebuilds all four 162-row source-W candidate classifications and their
   candidate/classification digests using exact rational arithmetic;
4. reconstructs the four-chart census and both frozen-prefix/all-signature
   queue scopes;
5. enforces canonical, type-sensitive strict JSON.

The verifier passes.  All 17 semantic attacks and all 7 strict JSON/encoding
attacks are rejected.  Producer and verifier outputs are byte-identical under
different hash seeds.

## Strict nonpromotion

```text
all disconnected exterior sheets excluded     false
all chart/grazing strata glued or typed        false
all return signatures exhausted                false
D02                                           BLOCKED
D03 negative oracle                      UNAUTHORIZED
Global Gate5                                  10/18
global complete 18-field blocks                   0
CM2                                  NO-GO_FOR_CLAIM
```

Next, reconstruct owner and outgoing-chart prefixes on the 19,686 remaining
unique leaves, type the 32 outside-`W:W` tangency strata, and subdivide the
38,180 outside-`W:W` multi-candidate leaves.  The same terminal census must
then be extended through all compact angular charts with unresolved leaves
equal to zero.
