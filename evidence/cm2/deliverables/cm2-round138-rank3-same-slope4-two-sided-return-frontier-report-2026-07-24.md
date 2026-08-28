# CM2 Round 138 — same-slope-four two-sided return frontier

Date: 2026-07-24

Round 138 freezes two positive-width local return cylinders on one common
implicit slope-four parent leaf. The minus/BYPASS square has first return
depth 298; the plus/HIT square has first return depth 349.

This closes an actual two-sided local return geometry around one D=0 event.
It does not construct a global Round35 restriction, canonical connected
component rank, short cell, image recut, Round50 owner, Round54 token, or
Round67 `q_j`.

## Common implicit parent leaf

The frozen source is core 14 on sheet `W:E`, with first target `W[1,0]`.
The source coordinate uses

```text
n(t) = (+sqrt(1-t^2), t)
r(t) = (4/25) asin(t)
v    = asin(p) - 4r.
```

At fixed

```text
p_star = -1587/1638400,
```

4096 exact rational bisections isolate the unique fixed-`p` D=0 root.
The common leaf parameter is the interval-defined object

```text
b_star = asin(p_star) - (16/25) asin(t_star).
```

It is frozen in a directed dyadic enclosure with 4104 fractional bits. Two
2048-step bisections then isolate the side levels

```text
D = -(4/25)^2 2^-128   (BYPASS)
D = +(4/25)^2 2^-128   (HIT).
```

The strict order is

```text
BYPASS root < D0 root < HIT root.
```

On the whole common parent interval, `D_t`, `D_p`, `dp_b/dt`, and
`dD/dt` along the leaf are all strictly positive. Thus increasing `t` is the
plus/HIT direction and decreasing `t` is the minus/BYPASS direction.

The frozen local parent identifier is

```text
round138-local-slope4-parent-W:
216354a2f6fa10bf6b674038aad2d5dc1f80ea0b4c97d973864d0dc03209412c
```

## Two exact graph segments and rational squares

Each side moves exactly `2^-1800` from its side-level root toward D=0. The
leaf value at the new `t` center is rounded to the unique nearest multiple of
`2^-4096`. Around that fixed rational center, Round 138 takes a square of
half-width `2^-2400` in both `t` and `p`.

For each side:

```text
exact graph t-length:       2^-2399
rational-square area:       2^-4798
graph strictly in square:   yes
square strictly in strip:   yes
```

The BYPASS graph and square satisfy `-SHIFT < D < 0`; the HIT graph and
square satisfy `0 < D < SHIFT`. Both use the same implicit `b_star` and the
same local parent-W identifier. Neither is a fixed-`p` box.

## Complete first-return replays

Every row carries two independent collision-owner accounts:

- the frozen retained-candidate universe, with 55 or 57 candidates;
- the full radius-four lattice universe, with exactly 161 candidates.

The selected winner agrees in both accounts at every collision.

| Side | Return depth | Retained histogram | Retained tests | Full tests | Terminal target |
|---|---:|---:|---:|---:|---|
| BYPASS | 298 | `55:95, 57:203` | 16,796 | 47,978 | `W[1,10]` |
| HIT | 349 | `55:117, 57:232` | 19,659 | 56,189 | `G[-3,-6]` |

The terminal C24 cores are:

```text
BYPASS:
core:1f2ba5184f0fb0d3879e6af889710cd0c41b98b1227b8f97bb706c42791a6f61

HIT:
core:f8b025dd81d1bdf83339ceb4295c431494540d9ab25a1dff45221614644874b8
```

All earlier 645 rows are strict C24 nonreturns; the two terminal rows are
strict returns.

Every official word is rebuilt after exact incoming-lattice translation
normalization. The first three ordinals are:

```text
BYPASS: 266945 / 285659 / 41371
HIT:    266945 / 285659 / 42355
```

Each side has 86 unique official-word IDs. Their ordered-sequence hashes are:

```text
BYPASS  0ff6b6a1c29afaf10b6697fcb0b31913ff2e7fb1674d5e631caf379dd2c6224e
HIT     901924e8522a6b97f4d02f1833fd79f053b566e935a9f334fdf2672407ef5e5c
```

The combined 647-row hash is

```text
d8c5dc0220511e1985d8d190e47392e8a790cd2100fab3d46042100bf9af8fb3
```

All 298 BYPASS collisions are central and have incidence rank 14. The HIT
path has 348 central collisions and one `H4294967295` collision. Its
incidence histogram is `14:347, 65:2`; the second rank-65 row is the next
collision's inherited source endpoint.

## Primitive-free Round132 crosswalk and time

Removing lattice translation `[0,1]` maps the local event to the unique
Round132 typed label

```text
["G", "W[0,-1]", 1, "W[0,-2]", -1].
```

The crosswalk deliberately excludes the Round132 primitive key, restriction
ID, and root coordinate. It uses only the primitive-free translated physical
event type plus an explicit collision timeline:

```text
time 0: source outgoing state
time 1: W[1,0]
time 2: G[0,1], current local event state
time 3: Round132 face insertion
```

Therefore the global insertion time is

```text
j = 2 prefix collisions + 1 face-local offset = 3.
```

The Round132 suffix offsets `{hit:1, miss:0}` align the post-face carriers;
they are not the insertion time.

The primitive-free event signature is

```text
round138-primitive-free-local-event:
107a74c77bf92a54fd7f8b9ea767f5814e01193cbdaefd6d799dc238d79edf90
```

## Independent verification

The verifier never imports or executes the Round138 producer and never reads
a temporary spike. It independently reconstructs the complete result using
only byte-pinned lower-round libraries and artifacts.

It performs full reconstructions at 12288 and 16384 bits. The two results are
identical, including all fixed rational centers, 647 rows, ledgers, IDs,
censuses, and nonpromotion fields.

Formal verification is `PASS`:

```text
re-signed semantic mutations rejected:  81/81
strict-JSON attacks rejected:           19/19
in-process path attacks rejected:       13/13
dual PYTHONHASHSEED replay:              byte-identical
process-level hostile I/O:               fail-closed
```

Frozen hashes:

```text
producer:            42d749dccea86aa3a122707db0226def176e75047d5dcb4bf19826b50e09282b
certificate:         c1f4d5041d810dd91d38e39bf795e5ab05536065ba8b0730530c58a91f7bf6d8
certificate result:  a46f4122639ccb82eed2d06d916972020b81c4f566ccfb05a9644de382a2e123
verifier:            7dfb9068696c5c868c614114c72e7c5819270c84c2c2455ad98f5e4f5321f941
verification:        1cd9878d03bde25bceb0dcf292d47783fe697de347ca653d1994b72a509015c3
verification result: 8dcfcc8c68fbf10ced13982f4fa86f480596f4b5d23db3351cc6afdcd0b399bb
```

## Strict global state

```text
common local parent-W roots:            1
positive-width local graph segments:    2
local return word-cells:                2
global Round35 restrictions:            0
global component ranks:                 0
global short cells / image recuts:      0 / 0
Round50 owners:                         0
Round54 t54 / pi54 maps:                0 / 0
Round67 Omega_j / q_j:                  0 / 0
global complete 18-field blocks:        0
Gate5 global maturity:              10/18
Gate5:                       NOT_CERTIFIED
CM2:                      NO-GO_FOR_CLAIM
```
