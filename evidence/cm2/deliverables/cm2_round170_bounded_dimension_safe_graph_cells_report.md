# CM2 Round170 — bounded dimension-safe graph-cell exploration

Date: 2026-07-26

## Verdict

`PARTIAL`.

Round170 is a bounded exploratory artifact, not a formal core-gate
promotion.  It keeps the official Round168 ledger unchanged:

```text
whole-record excluded   73,162
conservative live        3,670
official Round170 integer credit delta = 0
D02 = BLOCKED
CM2 = NO-GO_FOR_CLAIM
```

The producer is a normal deterministic rewrite of the preceding throwaway
spike, but its results remain nonpromotional.  In particular, neither a
depth-14 child count nor a rational volume may be folded into the integer
count of the 2,616 original Round168 owner-active parents.

## Replay scope and verification contract

The producer replays the full pinned Round166 depth-8→14 owner-active tree:

```text
depth-8 owner-active parents        2,616
evaluated tree boxes              167,984
evaluated active-root records     415,570
prior terminal child boxes        28,520
depth-14 unresolved frontier      56,780
```

The verifier does not import the Round170 producer.  It does import the
pinned Round165 and Round166 producer modules, replays the full tree relative
to those pins, and separately re-evaluates all Round170 classifications.
Therefore it is independent of the Round170 producer, but it is not
algorithmically independent of the upstream Round166 tree implementation.
This limitation is one reason the verdict remains `PARTIAL`.

The verifier checks the full canonical expected result, recomputes key
digests, rejects 20/20 re-signed semantic attacks and 7/7 strict-JSON
attacks, and explicitly rejects any child/volume-to-whole-parent integer
conversion.

## Three ledgers that must not be mixed

### 1. Depth-14 frontier records

```text
input                                      56,780
whole depth-14 records excluded             6,250
whole depth-14 records live                 3,590
typed/mixed analytic partitions             2,900
semantically closed                        12,740
residual                                   44,040

6,250 + 3,590 + 2,900 + 44,040 = 56,780.
```

The 6,250 and 3,590 are child-record counts.  They are not additions to the
Round168 integer census.

### 2. Rational depth-8-parent-equivalent volume

The Round166 frontier has exact volume `14195/16` in units of one original
depth-8 parent.  Round170 profiles it as

```text
excluded volume          917955/8192
live volume              506727/8192
mixed analytic volume        725/16
classified total         897941/4096
residual                2735979/4096

897941/4096 + 2735979/4096 = 14195/16.
```

These are rational volumes, not integer records.

### 3. Original Round168 depth-8 parents

A parent counts as fully replaced only if every one of its depth-14
descendants is closed.  The replay finds

```text
input owner-active parents                           2,616
fully replaced by the prior depth-14 tree              376
newly fully replaced by bounded Round170 blocks          78
fully replaced total                                   454
still not fully replaced                             2,162
```

The 454 split into

```text
whole-origin excluded                  182
whole-origin live                      236
resolved mixed/analytic partition       36
```

The 182 exact origin keys are only a formalization candidate for a later
round.  Round170 claims zero official integer credit and does not alter the
Round168 ledger.

## Bounded blocks

### A. Outgoing `H=0` seams

All 7,510 seam parents close, with no residual:

```text
whole parent excluded                 2,550
whole parent live                     2,180
typed/mixed analytic partition        2,780
```

The analytic partition is always dimension-safe:

```text
H<0 or H>0 open side     dimension 3
H=0 half-open graph      dimension 2
opposite open side       dimension 3
```

The graph has the pinned half-open owner `W`.  It is never counted by itself
as a whole-record exclusion.  Only 52 parents require further subdivision;
all close by two additional normalized `t/p` levels.

### B. Typed tangency collars

Of 1,220 input collars, exactly 1,000 satisfy all of:

```text
Delta<0 open side   excluded
Delta=0 graph       excluded
Delta>0 open side   excluded
```

Only because all three strata are excluded is the full depth-14 child
classified as excluded.  The remaining 220 need a tangency/outgoing-seam
double-graph arrangement and receive no credit.

### C. Same-sign monotone discriminant boxes

For a single target,

```text
dDelta/dp = 2*transverse*ell/sqrt(1-p^2).
```

When this derivative has a fixed nonzero sign and both `p` faces have the
same strict `Delta` sign, there is no `Delta=0` graph inside the box.  This
removes interval dependency overwrap for 4,076 boxes:

```text
whole parent excluded                 2,598
whole parent live                     1,358
follow-up H analytic partition          120
residual                                  0
```

### D. Source grazing in compact `q`

The exact compact coordinate is

```text
q = sqrt(1023/262144) r
p = sign * sqrt(1-(1023/262144)r^2)
r in [0,1].
```

The grazing face `r=0` is recorded separately as dimension 2; the interior
`r>0` is dimension 3.  Eight compact-coordinate refinement levels give

```text
input depth-14 grazing parents                     1,632
whole parent excluded                                102
whole parent live                                     52
parent residual                                    1,478

classified baseline-parent-equivalent volume   92437/4096
residual baseline-parent-equivalent volume      12011/4096
```

The two-dimensional face is not counted as volume.

## Hard residual

```text
multi-Delta arrangements (2–5 graphs)                    10,802
full-p Delta graph plus first-root equality sheet         4,812
tangency/outgoing-seam double graph                         220
compact-q grazing parents with residual cells             1,478
clipped/face-overwrapped single-Delta graphs              26,728
total                                                     44,040
```

The decisive obstruction is arrangement geometry, not raw rectangular
depth.  The next technical step is a parametric interval-Newton arrangement
for discriminant, first-root equality, outgoing seam, and compact-`q`
surfaces.  The 182 whole-origin-excluded exact keys should be formalized in a
separate round before any official ledger update.

## Artifact identities

```text
producer SHA256
952ac26c6729a02e3c5c364c8dda89cdc19b756ac46f7d5da01786fa1b7ca75f

certificate file SHA256
1a6fbab5676dc7e5ec91e5222810e34cfcc788517681e67441a1046e45ac62b8

certificate result_sha256
3497231e62539574bb5610df4024f1d06a6a40d787a08e089427c028678c4117

verifier SHA256
4a3807838fe1033adc6f5d05bb3fc4b49744034b6e8f2bce4ace71e27f2ae297

verification file SHA256
962d0f3fb86031ebc31d0808c5d0afd112d8796261652c720e1920246700a9c6

verification result_sha256
70510d463dac73ad7eee775b0f4e3792d24b90be8f984894b651cdb0e6412b8b
```
