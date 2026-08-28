# CM2 Round 140 — Round35 parent-W R1648 materialization audit

Date: 2026-07-24

Round 140 materializes the maximal legal portion of the Round35 parent-W
payload carried by the final Round139 positive-area fixed-`s` R1648 word
cell.  It does not mint a historical Round27 component ID, a historical
Round35 source-interval rank, a natural `1e-90` short-cell index, or a
Round35 parent-W/restriction ID.

## Frozen final Round139 boundary

The producer pins all three final Round139 files:

```text
Round139 producer:
462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b

Round139 certificate:
64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0

Round139 verifier:
cb96e0e1a74abcac4254f20584bab6997edb8de69f0d979f1d65d4c3fdfadd09
```

The final Round139 certificate supplies one positive-area rational rectangle
at `s=0`, a positive-width exact slope-four leaf subgraph inside that
rectangle, and a strict first-return word of depth 1648 on the whole
rectangle.

## Legally materialized source/path tuple

The Round27-compatible payload schema is

```text
[source_core_id, return_depth, [official_word_key_id_1,...,official_word_key_id_n]]
```

and the materialized values are:

```text
source core index:                  14
source core ID:
core:90398e9ab632e57b027266bc7c34461a0a6a6d308c35fbeacc41432a3d7f48f7

return depth:                       1648
official-word occurrences:         1648
unique official-word IDs:          141
ordered official-word SHA256:
f504289edce554d47e17a90d7c886586a69f3ec4b64fafd90c718c50ca93221e

complete source/path tuple SHA256:
5cec1061ec331e8f37929dfb1b2b2a78757309ba60198d571abd9e8cf6c70ed9
```

The first and last official words are, respectively,

```text
gate5-word:266945:f86c66902f1acc76521086a8d15abc55cf7a1d77a13bf03fb64dffbf9eb47ea8
gate5-word:291560:6c7c484df06c7e03aef7e83aa2fe403090d4843175262deb78c507154f349115
```

The certificate contains all 1648 IDs, not only their digest.

## Fixed parameter and implicit leaf

The exact descriptor is

```text
s = 0
p_star = -1587/1638400
b_star = asin(-1587/1638400) - (16/25) asin(t_star),
```

where `t_star` is the unique root in the published Round139 deep-D0 bracket
of the collision-3 `W[0,0]` discriminant at fixed `p_star`.  The contact
coordinate is `r=(4/25)asin(t)`, so the same leaf is

```text
asin(p) - 4r = b_star.
```

The 16448-fractional-bit directed dyadic outer is retained only as an
enclosure of this implicitly defined real.  It is not substituted for
`b_star`.

Exact-array canonical digests are:

```text
deep-D0 root bracket:               9aa1106a9270ec3de4845680a12f34f515d1d047593a1e4ed04e94f7fd6a0b94
b_star directed dyadic outer:       df6a752e486c6cb615ed8a5c5591decdd85b8a1d0791056eca9a47e14ce92933
Round139 physical rectangle:        a267975d36c747d4a49471ebb22e979f5af94325e3229d07366cb70a7e91eb18
normalized open rectangle:          33ae06940215b91c324b84700d648b97301619fd695dc39d5dcdc183216ee284
```

The full exact rational arrays are in the certificate.

## Incidence path and Round35 mesh

Every one of the 1648 source and target capped reciprocal-cosine ranks is
14.  Hence

```text
incidence path:                     [14] repeated 1648 times
incidence path SHA256:              a2669f5587b2c7c10dc0d18fe1db2516df2b2049a7bf8cd37292636cd9c6fbe7
B:                                  14
ceil(3(B+1)/2):                     23
delta_14:                           1/8388608 = 2^-23
```

## Prospective Round137-v1 contained ranks

Using the exact Round137 affine normalization of source core 14, the
independent verifier searches levels in ascending order and then uses the
contract's primitive common-denominator lexicographic order.  The first
feasible level is 5883 in both dimensions.

The 2D row and rank are:

```text
row schema:                         (m,a0,a1,b0,b1)
level:                              5883
complete row SHA256:                d344625211da3e69aa0e43e77940de6d7023250017a670fab09a02e77cfeb427
rank bit length:                    23530
rank decimal digits:                7084
rank decimal SHA256:                81ee4f795045d8478e621dbcaf2cba2437ccb168b34b770f995c012c0060927f
locator:
round140-r1648-component-witness-locator:ebb0c5bf600c09b205eb8bc8c6e40f0e5c250874d14aff5c065091f1d94b665a
```

The 1D exact-leaf row and rank are:

```text
row schema:                         (m,a0,a1)
level:                              5883
complete row SHA256:                18bb8afd2331a7d2e9b07726bdb1323ddf0425888ea2a05e058173df51ca8294
rank bit length:                    11765
rank decimal digits:                3542
rank decimal SHA256:                fe02c53ca61c7ae9a81d189ffbf5d58cbae33ee16cb68e6248c65d5fc708c24d
locator:
round140-r1648-leaf-witness-locator:0ea1294fdcf8cb1915c4ff2c8c87312253d0afc8da23e88840bb64724ba73d18
```

Both complete rows and both complete decimal/hexadecimal ranks are stored in
the certificate.  These are the least Round137-v1 ranks contained in the
specific inner rectangle and known leaf subinterval.  They are only
upper-bound locators for the least v1 ranks elsewhere in the larger
connected return component and maximal U-intersection leaf interval.

## Natural short-cell blocker

The known exact leaf subinterval has H1 length strictly below `2^-5888`,
which is shorter than `1e-90`.  That fact does not determine a natural
short-cell index.

Round35 anchors the grid

```text
[k*1e-90,(k+1)*1e-90]
```

at an oriented endpoint of the maximal U-intersection leaf interval.
Round139 supplies only an interior subinterval.  It does not supply that
maximal endpoint, the oriented arclength origin, or the subinterval's
position relative to the endpoint-anchored grid.  Therefore:

```text
historical Round27 component rank:  null
historical Round35 interval rank:   null
natural short-cell k:               null
Round35 source parent-W ID:         null
Round35 image recut rank:           null
Round35 restriction ID:             null
```

## Independent verification

The verifier does not import or execute the Round140 producer.  It checks all
1648 Round139 collision-row closures and official-word closures, reconstructs
the complete path and incidence data, and independently implements the
Round137-v1 rank formulas and minimal-level/lexicographic proof.

```text
formal verification:                PASS
re-signed semantic mutations:       44/44 rejected
strict-JSON attacks:                16/16 rejected
in-process path attacks:             7/7 rejected
hostile process/I/O cases:          13/13 fail-closed
clean producer replay:              byte-identical
dual-hash-seed verifier replay:     byte-identical
```

Frozen hashes:

```text
producer:
6329e0050f6727f8c0fa7d2a5052028645a375c5d59c51169e2ec81fb2ad7377

certificate:
bb6283e2fccba194b47f9aa174e85594560ba88062ed57d06651003744755a79

certificate result:
7988f4c9588894ec964e2c6efec4dd07dd28d5011c0bf004ad73f99414534eed

verifier:
9494a893edf8ed136a0150d3919690b6fe84d438aadc00e5bb278a7b6ba6069e

verification:
b38306fb85e4a8a27d0339d95ff9e7ee3eabea044239972c719c926e0891782d

verification result:
9d898c0cea05069511732acd2be74f04d66f416d10f4ca72cd6e6bccf8b9cf33
```

## Strict global state

```text
historical Round35 parent-W IDs:     0
historical Round35 restrictions:     0
Round50 owner keys:                  0
Round54 t54 tokens:                  0
Round67 q_j outputs:                 0
global complete 18-field blocks:     0
Gate5 global maturity:           10/18
Gate5:                    NOT_CERTIFIED
CM2:                   NO-GO_FOR_CLAIM
```
