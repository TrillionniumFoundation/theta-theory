# CM2 one hundred forty-third direct assault

Date: 2026-07-24

Strict verdict: **the left terminal-face endpoint of the frozen
Round139/R1648 branch is now formally isolated and its local word/owner
history is complete, but the intervening face-to-D0 corridor is not yet a
certified maximal physical source leaf.**

## What closed

Round 143 proves a unique root of
`p_1648(lambda)=-1/50` for
`lambda=(x_star-x)2^4289`, with `1<lambda<2` and a strict negative
derivative over the exact root bracket.  Thus:

```text
2^-4289 < x_star-x_left < 2^-4288
```

The proof exhausts all 161 radius-four candidates at each of 1,648
collisions:

```text
candidate tests:                 265,328
strict margin facts:             292,473
worst margin depth:                4,284
preterminal nonreturns:            1,647
terminal active face:     G:S, p0=-1/50
```

The first direct interval attempt was fail-closed because wrapping could not
resolve one candidate discriminant at collision 1,054.  The final proof uses
an independently recentered two-generator affine propagation; it does not
drop or special-case the failed row.

## What became executable

The candidate face-to-D0 interval is shorter than both `delta_14=2^-23` and
`10^-90`.  Two explicitly normalized prospective Round137-v1 searches give:

```text
x=sqrt(17)r: level 4290, 8,578-bit rank, SHA256 2650e59e81848f02e30fabbce2cad195e95c979c8bc695a7f577ae9c73ffb1c9
u=100t-1:    level 4283, 8,565-bit rank, SHA256 da159470a46c7e5b75b099dda6c7aa939daee12b72fb47b471f08f8ea549eaa0
```

Their differing levels prove that a historical coordinate crosswalk cannot
be inferred.  The candidate is conditionally one clipped `B14` cell and one
clipped `10^-90` source cell, with prospective left-anchored `k=0`.

The formal image expression gives a conditional `10^-90` recut count of

```text
18482025737079285768196755871683993421335748959797565447882270854942728583699291803410531
```

with rank range `[0,count-1]`.  This is a deterministic prospective ledger,
not the historical Round35 image-recut rank.

## Independent assault

```text
producer SHA256:        bac63d0fb61965030a38b02f213ca90f580b66fc1f163f4829f2dafb57193a38
certificate SHA256:     74df2697c0db44ea5ac0a3ea9ab360100fc9750e1358b5172cd359522886ef67
certificate result:     35a9f8e0437086a2feaf294c10c621ce21319dc93aac88f33dbc4024e4507e92
verifier SHA256:        197be350c4a6bed80a1c413822c5b838c2d0bc7da88360998fd7ad939da85601
verification SHA256:    3ee6fe0e48bdf05a6f76726ded302aa4d632c306a4a260f444e1c2a66dfd9bd7
verification result:    51d616892452c92a4ed47586b6923ffaaf8e722e6b32d48445cbb4f762f9cf1c
```

The two producer seeds were byte-identical.  The verifier rejects all 30
semantic mutations and independently replays the producer byte-for-byte.
External hostile tests rejected `8/8` strict-JSON inputs, `7/7` producer
output paths, `7/7` verifier output paths, and `5/5` process-level hostile
certificate inputs.

The exploratory path harness once targeted the producer's legal canonical
output and wrote a sentinel.  That invalid case was removed; the exact
certificate was restored from the already byte-identical independent replay,
its expected hash was revalidated, and a fresh complete verifier replay was
run after restoration.  The final manifest is therefore post-restoration.

## Exact remaining door

The new local face root is separated from the Round139 certified D0 collar
by a scale-`2^-4289` interval.  There is still no connected certificate that
every point in that corridor retains the same 1,648-word owner sequence and
nonreturn inequalities.  Without it, the candidate cannot be identified as
the maximal physical `U`-intersection leaf, and none of the historical
Round35 identifiers can be assigned.

```text
historical component rank / ID:     null
historical source interval rank:    null
historical short-cell k:            null
historical parent-W ID:             null
historical image recut rank:        null
historical restriction ID:          null
global complete 18-field blocks:       0
Gate5 maturity:                    10/18
Gate5:                    NOT_CERTIFIED
CM2:                   NO-GO_FOR_CLAIM
```
