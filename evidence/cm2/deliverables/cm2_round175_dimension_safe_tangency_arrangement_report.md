# CM2 Round175 — dimension-safe tangency arrangement

Date: 2026-07-26

## Decision

Round175 reconstructs the 22 tangency-parent composites left live by
Round172 and materializes their frozen-prefix discriminant and outgoing-chart
arrangements without converting lower-dimensional strata into integer record
credit.

```text
Round172 input tangency composites             22
fully excluded parents                          6
fully live parents                              0
mixed residual composites                      16
  frozen-owner tangency parents                14
  mismatch-target exceptions                    2
physical source-chart cross-seam parents        2
```

Only the six parents whose every physical stratum is a frozen-prefix
mismatch receive one new whole-parent exclusion each.  All 16 mixed parents
retain both a strict live open witness and a strict mismatch open witness, so
none can be promoted to a whole-parent exclusion.

## Exact six-parent credit set

```text
W:E:01.12.1111010
W:E:01.13.0101010
W:E:03.07.01100
W:E:04.08.10011
W:E:06.02.1010101
W:E:06.03.0000101
```

All six parents are strictly inside the physical source chart.  There is no
source-chart seam and no rational-guard-outside slice in any credited
parent.  The independent verifier reconstructs the complete stratum coverage
for every key:

```text
Delta < 0 open side     frozen owner W[1,0] absent: mismatch
Delta = 0 graph         W-owned tangency, but outgoing H sign mismatches
Delta > 0 open side     W first, but outgoing H sign mismatches
relevant H = 0          empty on the whole parent
source chart seam       empty on the whole parent
guard-outside slice     empty on the whole parent
```

The relevant outgoing function is strictly signed throughout each credited
parent and has a strictly negative p derivative.  Three credited parents use
`H_NW<0` as the mismatch sign and three use `H_SW>0`.  Consequently no
unaccounted H-zero seam, Delta-H intersection, boundary corner, source seam,
or guard slice remains inside any of the six integer-credit units.

## Sixteen exact residual arrangements

The other 16 parents remain conservative composites.  Each has:

```text
ambient parent dimension                         3
Delta-negative open side dimension               3
Delta-zero graph dimension                       2
Delta-positive open side dimension               3
outgoing H-zero graph dimension                  2
H graph p derivative               strictly negative
H graph half-open owner                           W
boundary clipping/grazing nominal dimension      1
integer credit for internal analytic strata      0
strict W-live open witness                     present
strict mismatch open witness                   present
```

For the 14 frozen-owner tangency parents, the discriminant orientation is:

```text
Delta < 0       frozen owner absent: mismatch
Delta = 0       W-owned tangency graph
Delta > 0       W-first side
```

Their Delta-H intersection is empty.  On `H=0`, the diagonal-contact chord
satisfies

```text
|dot(D,m)| > 1/sqrt(2) - 2 R_W > 19/50,
```

which places the H graph strictly inside the `Delta>0` W-first side.

The 2 Round164 regression exceptions are not assigned the owner-graph
orientation mechanically:

```text
W:N:05.00.00100110       tangency target G[1,1]       relevant H_NW
W:S:H.05.00.00100110     tangency target G[1,0]       relevant H_SW
```

For each exception the rederived orientation is:

```text
Delta < 0       mismatch target absent; contains frozen-W live region
Delta = 0       mismatch-target tangency graph
Delta > 0       mismatch-target-first side
```

An independent adaptive `(t,s)` base partition produces 18 terminal cells
per exception, with maximum extra depth 6.  Exact rational p brackets keep
the Delta and H graphs strictly ordered on every terminal cell, conserve the
entire base area, and certify `Delta intersect H` empty.  The H graph lies on
the mismatch target's `Delta<0` side.  The two terminal-cell table digests
are:

```text
W:N exception
299e81f4b87a986325bcbd182cd54eaf44bc6fedfd79bf3f07252bbbd41ef922

W:S exception
7fe3f20df256d4ba0acd1701a322e335b432b4c060a8f777fa28f0dd59691291
```

## Physical source seam versus rational guard

The physical source-chart seam is the irrational analytic surface
`2*t^2=1`.  It is distinct from the atlas's rational guard band
`[-177/250,177/250]`.  Exactly two parents cross the physical seam:

```text
W:E:00.15.0000000
W:E:07.00.1111111
```

In each, the physical E-chart interior and the guard-outside slice both have
positive volume.  The guard-outside slice is a chart-domain rejection that
requires neighboring-chart recoordinatization; it is not an exterior
exclusion and receives zero integer credit.  The physical source seam is a
real two-dimensional stratum, half-open owned by E under the pinned rule
`E or W owns; N or S excludes`.  Its nominal one-dimensional intersections
with Delta and H also receive zero integer credit.  Both cross-seam tubes
therefore remain among the 16 residual composites.

## Composition with Round172

Round175 adds exactly six credits inside the 22-parent Round172 live block.
The credit keys are distinct from all Round172 credits.

```text
Round172 whole-record exclusions                  73,172
Round175 new whole-parent exclusions                   6
combined whole-record exclusions                  73,178

original prefix stage-one matches                    518
Round165 seam live composites                        504
Round175 mixed tangency composites                    16
Round166 owner-active multi parents                2,616
combined conservative live                         3,654

conservation                              73,178+3,654=76,832
```

The authoritative refined source-W record total remains 76,832.  Delta-zero
graphs, H-zero seams, Delta-H intersections, boundary corners, source-chart
guard slices, the 16 internal mismatch portions, Round165 typed collar
sides, and the Round166 unverified deep profile all receive zero additional
whole-record credit.

## Independent verification

The verifier byte-pins but does not import or execute the Round175 producer.
It independently decodes all 22 dyadic parent paths, replays every retained
candidate root and physical tangency graph at 192-bit Arb precision,
recomputes outgoing H values and derivatives, re-finds all strict open
witnesses, rebuilds both adaptive exception partitions, and reconstructs the
full expected certificate.

It requires recursive exact-key equality and full expected canonical
document equality.  Its credited-parent audit separately records the
Delta-negative, Delta-zero, Delta-positive, H-zero, physical source-seam, and
guard-outside disposition of each of the six credited keys.

The fail-closed suites pass:

```text
re-signed semantic mutations rejected             156/156
strict JSON attacks rejected                          9/9
path-safety attacks rejected                          7/7
```

The semantic suite includes a separate mixed-to-excluded forgery and live
open-witness deletion for every one of the 16 mixed parents, a separate
fake-mixed mutation for every credited parent, guard-outside credit
forgeries, exception graph-order and terminal-cell mutations, complete
census and ledger mutations, recursive extra-key injection, provenance-pin
mutations, and D02/CM2 promotion attempts.  Every semantic candidate is
re-signed at the result-envelope level before rejection.

The strict-JSON suite rejects duplicate envelope and nested keys, floating
and exponent numbers, NaN, BOM, raw NUL, invalid UTF-8, and noncanonical
whitespace.  The path suite rejects symlink, hardlink, and oversized inputs,
plus symlink, hardlink, protected-alias, and outside-directory outputs.

Cold replay in separate clean processes under `PYTHONHASHSEED=1` and
`PYTHONHASHSEED=987654321` is byte-identical for both the certificate and
verification:

```text
producer source SHA256
16122dcc7c39b140d45139a01bac6d6f41d7cbb60da2499ecc50fbeac2766355

certificate result SHA256
827d6f674dd4a5291bf08f5ffd65b31187faa1c9fe977e1b7e7da10cd1166d72

certificate file SHA256
a2a69b3d4559fadb647d8f9ea6a06ef4c1625647965423cdb25f53fa08d2deee

verifier source SHA256
2c8a5906806adef423ba5d409cbf294c4988db72a1b9cfdf26a61ee9a7d290e6

verification result SHA256
ed5fd96874a65b49a1e05d5589e2dd9711f224d08a99123e582bc54bce294f6a

verification file SHA256
6f1d8e515be0cdc977445e7e0d8633df510c793ff99e0f76cf3b4578d2d2bfca
```

## Strict state and next gate

```text
D02                                      BLOCKED
D03 negative oracle                     UNAUTHORIZED
Global Gate5                            10/18
global complete 18-field blocks             0
CM2                                      NO-GO_FOR_CLAIM
```

The next core tangency work is to isolate boundary-clipping and physical
source-chart cross-seam residual strata in all 16 mixed composites, then
continue later frozen-prefix processing only on certified live strata.  The
224 whole-W rectangles and 2,616 owner-active multi parents also remain
downstream core work.
