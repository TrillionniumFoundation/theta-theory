# CM2 Round165 — adaptive outgoing-chart seam census

Date: 2026-07-26

## Decision

Round165 resolves the outgoing dominant-chart classification on all 618
Round163 seam-overwrapped owner-matching parent leaves.  It produces 118
whole-parent outgoing-chart mismatches, 220 whole-parent first-stage W
matches, and 280 dimension-safe typed seam partitions.  The adaptive
depth-limit residual is zero, and only four parents require one bisection.

This is a recordwise result for the frozen first collision
`owner=W[1,0], outgoing chart=W`.  It is not exterior-sheet exhaustion, does
not resolve later return-prefix stages, and does not close D02.

## Dimension-safe baseline

The producer pins the corrected Round164-v2 certificate and verifier.  It
inherits no whole-leaf exclusion from a codimension-one tangency graph:

```text
Round163 recordwise excluded baseline       37,480
Round163 ambient remaining baseline          39,348
Round164 full-dimensional new exclusions          0
Round164 tangency ambient parents                 32
```

The 32 tangency parents retain unresolved off-graph ambient bulk.

## Exact seam classifier

For the same-colour flight from source W to target `W[1,0]`, source and
target translate together.  Their relative centre is exactly `(1,0)`, so
the entire owner flight and outgoing seam test are independent of `s`.

For either W-adjacent diagonal target normal `m`, define

```text
D_m = (1,0) + R_W m - R_W n_source
H_m = cross(u,D_m).
```

On a forward incoming intersection,

```text
H_m=0  iff  the near-contact target normal is m
partial_p H_m = -dot(u,D_m)/sqrt(1-p^2) < 0.
```

The two seams are

```text
NW: m=(-1,+1)/sqrt(2),  n_x+n_y=0
SW: m=(-1,-1)/sqrt(2),  n_x-n_y=0.
```

The tight contact reconstruction first cancels the common translation and
then uses the orthonormal-frame identity

```text
n_out = (-sqrt(Delta) u - transverse J u)/R_W.
```

This removes the duplicate interval cancellations in the Round163
`q+tau*u-centre` expression while replaying the original Round163 expression
separately for frozen row-digest identity.

A seam collar is never credited as a whole-leaf exclusion.  Each accepted
collar materializes three strata:

```text
3D W open side                 frozen stage-one match
3D adjacent N/S open side      outgoing-chart mismatch
2D diagonal graph              W-owned half-open seam
```

The W ownership is fail-closed against the pinned Gate3 chart-seam quotient
manifest, including its assertion that the half-open ownership rule applies
to analytic strata.

## Census

Input parent leaves:

```text
W:E    468
W:N     75
W:S     75
W:W      0
total  618
```

Parent-level resolution:

```text
whole-parent outgoing-chart mismatch          118
whole-parent W first-stage match               220
parent with typed three-stratum seam partition 280
depth-limit residual parent                      0
```

The 618 parents become 622 terminal rectangle-or-collar records:

```text
strict normal-margin mismatch rectangles        60
monotone-H-separated mismatch rectangles         58
strict normal-margin W rectangles               124
monotone-H-separated W rectangles               100
typed seam collars                              280
depth-limit unresolved                            0
```

The typed graph census is exactly symmetric:

```text
NW graphs                  140
SW graphs                  140
full p-graphs               10
monotone clipped graphs    270
```

The maximum permitted extra depth is 14, but the maximum used depth is 1.
Exactly four parents split once; all other parents terminate without further
subdivision.

The exact input rational volume is

```text
155937/102400000.
```

Its dimension-safe terminal split is

```text
whole mismatch rectangles     7611/102400000
whole W rectangles           143901/204800000
typed seam collars           152751/204800000.
```

The conservative rectangle-or-collar record ledger replaces 618 old seam
parents by 622 terminals:

```text
refined source-W total records       76,832
refined whole-record exclusions      37,598
refined conservative live records    39,234.
```

The 280 mismatch open sides inside typed collars are explicit analytic
strata, but are deliberately not mixed into the whole-rectangle exclusion
count.

## Verification

The independent verifier does not import or execute the Round165 producer.
It independently rebuilds:

```text
Round163 owner rows                 1,176
Round165 seam parents                 618
Round165 terminal records             622
typed three-stratum partitions        280.
```

It reconstructs the full expected certificate document, recursively checks
exact keys at every dictionary/list layer, recomputes all sign labels and
dimension-safe ledgers, and requires canonical equality.  It passes with:

```text
resigned semantic attacks rejected   46/46
strict JSON attacks rejected           7/7.
```

Cold replay under distinct hash seeds is byte-identical:

```text
producer source SHA256
95bdbe3fc8d1d26512d8469a0e9382a3e977d5606375ed2729877c9f1ac8e012

certificate result SHA256
93e2899d0a9a79a82e1b193158f3733e891e2c5b4c9ce83f970aff40bf75c270

certificate file SHA256
2cbd69e8cbde66966d78764c0d5b34518c2ec55891d0238a62f40073ae4876a8

verifier source SHA256
1967147d98075792dc6821ff72e46b2f33251ba98950d1660d10280bf0ef298e

verification result SHA256
86356b4b778fc8e2f74ab1edec30c96346027a9c17ade38c6f5aef269d6e5786

verification file SHA256
af684b956c40c97e26fdd5f9ddacea85b9c693b0b9a935d387ed1a5142ffa3b5
```

## Strict state and next gate

```text
Round165 outgoing seam depth residual    0
Round164 tangency off-graph parents      32
outside-W:W multi-candidate parents  38,180
D02                                  BLOCKED
D03 negative oracle                 UNAUTHORIZED
Global Gate5                        10/18
global complete 18-field blocks         0
CM2                                  NO-GO_FOR_CLAIM
```

The next dimension-safe gate is to materialize the `D<0`, `D=0`, and `D>0`
replacements of all 32 Round164 tangency parents, then resolve the 38,180
outside-`W:W` multi-candidate leaves.
