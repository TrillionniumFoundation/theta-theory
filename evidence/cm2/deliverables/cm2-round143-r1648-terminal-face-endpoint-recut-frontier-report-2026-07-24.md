# CM2 Round 143 R1648 terminal-face endpoint and recut frontier

Date: 2026-07-24

## Verdict

Round 143 certifies one exact local endpoint of the frozen Round139
fixed-`s=0`, fixed-`b`, slope-4, depth-1,648 branch.  In the scaled coordinate

```text
lambda = (x_star - x) 2^4289
```

the equation `p_1648(lambda)=-1/50` has exactly one root in the recorded
bracket, `1 < lambda < 2`, and
`d p_1648 / d lambda < 0` throughout that bracket.  Equivalently,

```text
2^-4289 < x_star - x_left < 2^-4288.
```

This is a certified local terminal-face endpoint, not a certification that
the entire face-to-D0 interval is one maximal `U`-intersection leaf.  The
historical Round35 source interval, parent `W`, short-cell index, image recut
rank, and restriction remain null.

## Frozen inputs

The producer fails closed unless the final Round139 and both final Round140
chains retain their pinned bytes.  The principal pins are:

```text
Round139 producer:       462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b
Round139 certificate:    64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0
Round139 verification:   57093537ae3f464e276da830ee5821ffbe3576278c71adbe111b22a128f3005f
Round140 bridge source:  838d5ffbedd88856df561f5b6343d63466d03cab89189b3bc4eb4838f65ad4e2
Round140 bridge cert:    e3f08525e770829c3ce71fed872a18dbfdc3139f514c3f865d12f6abc114a353
Round140 parent source:  6329e0050f6727f8c0fa7d2a5052028645a375c5d59c51169e2ec81fb2ad7377
Round140 parent cert:    bb6283e2fccba194b47f9aa174e85594560ba88062ed57d06651003744755a79
```

Round139, Round140, Round141, and Round142 artifacts were not edited by the
Round143 producer or verifier.

## Formal endpoint proof

The discovery phase uses 24,576-bit dual arithmetic for four Newton locator
iterations.  The formal phase is separate: it propagates a two-generator
recentered affine model in `lambda` and `t_star` at 12,288 bits, recenters at
every collision, and proves the terminal sign order and strict derivative on
an exact bracket of width `2^-1535`.

The terminal owner is:

```text
absolute owner:  G[-7,-13]
terminal chart:  G:S
destination:     core:e47f553e056452faa012129434cdbbb6a55cd9671a19ea04e6b8a9f43054c4c2
active face:     p0=-1/50
```

The complete radius-four universe was checked at every collision:

```text
collisions:                         1,648
candidates per collision:             161
candidate tests:                   265,328
strict margin ledger entries:      292,473
worst strict-margin dyadic depth:     4,284
preterminal strict nonreturns:        1,647
terminal active faces:                    1
```

The margin-kind ledger is:

```text
candidate_miss_discriminant          249435
candidate_positive_discriminant       15893
candidate_behind_far_root               7937
candidate_future_root_positive          7956
winner_pairwise_root_gap                6308
selected_discriminant_positive          1648
selected_root_positive                  1648
selected_root_below_tau_max             1648
```

An earlier direct interval propagation was rejected at collision 1,054 for
candidate `G[0,2]`: wrapping left the discriminant interval with radius about
`0.162`, so it could not prove the required sign.  No row was skipped.  The
formal recentered affine model was introduced specifically to remove that
dependency blow-up and completed the full ledger.

The final implementation records a conservative dyadic depth directly from
the exact Arb lower endpoint mantissa and exponent.  This avoids hundreds of
thousands of unnecessary `Fraction` normalizations; it does not weaken any
strict sign test or change the certified lower bound.

## Candidate leaf interval and exact blocker

The new face root and the pinned Round139 D0 endpoint give the prospective
open interval `(x_left,x_star)`.  Its adapted source line element is

```text
dell_* = (25/4+4)|dr| = 41/(4 sqrt(17)) dx.
```

Its exact outer length is below both `delta_14=2^-23` and `10^-90`.
Nevertheless, the pinned chain certifies the frozen word only on the
Round139 `2^-5888` collar and locally at the new face root.  It does not
contain a validated connected all-owner/nonreturn cover of the intervening
scale-`2^-4289` corridor.  Therefore:

```text
whole interval has certified owner corridor:         false
whole interval equals maximal U-intersection leaf:    false
```

This is the first strict blocker and is preserved verbatim in the
certificate.

## Coordinate-explicit prospective ranks

For the candidate interval, Round 143 computes the least contained
Round137-v1 consecutive dyadic pair separately in two explicitly declared
coordinates:

```text
coordinate                    level   rank bits   digits   decimal SHA256
x=sqrt(17)r                    4290       8578     2582   2650e59e81848f02e30fabbce2cad195e95c979c8bc695a7f577ae9c73ffb1c9
u=100t-1                      4283       8565     2579   da159470a46c7e5b75b099dda6c7aa939daee12b72fb47b471f08f8ea549eaa0
```

The different levels are an executable witness that the historical leaf
coordinate has not been frozen.  These are prospective coordinate-specific
locators, not the unnamed historical Round35 source-interval rank.

At incidence rank `B=14`, the whole candidate interval would be one clipped
`B14` source cell and one clipped `10^-90` source cell.  With its own left
endpoint as the prospective oriented origin, the conditional short-cell
index is `k=0`.  Historical `k` and historical parent-`W` remain null because
the maximal physical interval and its historical origin have not been
materialized.

## Conditional image recut ledger

The formal image endpoint expression is

```text
asin(t_right)-asin(t_left)+asin(p_right)-asin(-1/50).
```

At deterministic scale `10^-90`, its conditional recut count is

```text
18482025737079285768196755871683993421335748959797565447882270854942728583699291803410531
```

It has 89 decimal digits, 294 bits, and decimal SHA256
`866cc155fbf90260eefa345d454f554ef920d297b9d58a2e6e283139907350ae`.
The conditional rank range is `[0,count-1]`.

That ledger becomes physical only if the missing full source corridor is
certified as one connected branch.  It is not a historical image recut rank,
and the D0 branch-limit image endpoint is not asserted to be an actual
regular trajectory.

## Independent verification and hostile tests

The verifier does not import the producer.  It independently checks the
closed envelope and pins, root-bracket order and width, complete ledger
reconciliation, preterminal/terminal scope, both rank formulas and
rank-unrank roundtrips, coordinate underdetermination, source mesh,
conditional image count, null historical fields, and strict Gate5/CM2
nonpromotion.  It then replays the producer in a clean temporary directory
under an independent hash seed and requires byte identity.

```text
formal verification:                      PASS
re-signed semantic mutations:            30/30 rejected
external strict-JSON attacks:              8/8 rejected
process hostile certificate inputs:        5/5 rejected
producer hostile output paths:             7/7 rejected
verifier hostile output paths:             7/7 rejected
dual producer hash seeds:            byte-identical
post-restoration verifier replay:           PASS
```

During development of the external hostile-output harness, one exploratory
case incorrectly treated the producer's canonical certificate destination
as a forbidden target.  That target is necessarily writable by the producer,
so the harness wrote a 13-byte sentinel.  The case was discarded, the
canonical certificate was immediately restored from the byte-identical
independent producer replay, and its SHA256 was re-established as
`74df2697c0db44ea5ac0a3ea9ab360100fc9750e1358b5172cd359522886ef67`.
The corrected harness uses only genuinely protected targets.  A complete
verifier replay was launched after restoration, and the final manifest was
built only after all canonical pins were rechecked.

## Final strict state

```text
local terminal-face endpoint count:           1
coordinate-specific prospective ranks:        2
historical Round27 component IDs/ranks:        0
historical Round35 interval rank:              0
historical Round35 short-cell k / parent W:    0
historical image rank / restriction:           0
Round50 owners / Round54 tokens:               0
Round67 q_j outputs:                           0
global complete 18-field blocks:               0
Gate5 global maturity:                     10/18
Gate5:                              NOT_CERTIFIED
CM2:                             NO-GO_FOR_CLAIM
```
