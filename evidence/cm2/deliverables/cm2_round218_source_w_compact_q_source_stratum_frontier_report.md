# CM2 Round218 — compact-q source-stratum frontier

Date: 2026-07-27  
Verdict: `BOUNDED_NONPROMOTIONAL_COMPACT_Q_FRONTIER__NO_WHOLE_ORIGIN_CREDIT`

## Scope

Round218 selects the frozen, outcome-blind `COMPACT_Q_PRESENT` cohort from the
Round184 source-W registry.  The selected set contains exactly 54 origins and
has ordered-key digest
`d5fd64dc6d287982b6bf6739295869a21991b758917754eea3aa55476e504e7b`.

The two Round212 source seams and all 198 remaining mixed origins are outside
this cohort.  They are neither imported into the compact analysis nor counted
again.

The compact source coordinate is

```text
q = sqrt(1023/262144) * r
p = sign * sqrt(1 - (1023/262144) * r^2)
r in [0,1].
```

The `r>0` stratum is 3D.  The grazing face `r=0` is retained as a separate 2D
stratum, with exact 1D edge and 0D corner ownership.

The complete canonical evidence document is materialized at
`cm2_round218_source_w_compact_q_source_stratum_frontier_result.json`.
It contains `1,961,083` bytes, has file SHA256
`dc4d86f68393736c314005aff27ea2febb8072e3224c892090d8a7cf54844887`,
and has result SHA256
`f440ee0ac043067a48b8ed8e217a827ed8c0e5072778e84931090df8cd4f7000`.
Its canonical object is exactly equal to both independent-seed probe
documents.

## Frozen outer reconstruction

The probe independently rebuilds:

```text
54 compact-q origins
114 Round176 preclosed frontier leaves
2,230 Round176 residual roots
21,334 Round180 final children
18,782 exact-behind geometrically closed children
2,552 geometric residual children
35,852 deleted exact-behind candidates
3,692 failed exact-behind candidates
```

The initial 2,230-root partition is:

| Category | Roots |
|---|---:|
| clipped/face-overwrap single Delta | 164 |
| full-p Delta/root-order | 762 |
| multi-Delta | 460 |
| compact-q source grazing | 844 |

The final 21,334-child partition is:

| Category | Children |
|---|---:|
| clipped/face-overwrap single Delta | 1,658 |
| full-p Delta/root-order | 8,428 |
| multi-Delta | 5,210 |
| compact-q source grazing | 5,862 |
| typed tangency/outgoing seam | 176 |

Only 26 origins retain a rectangular outer 3D residual after exact-behind
reduction.  The other 28 have zero such residual, but this does not close the
original source parent: all 28 still retain a 3D compact-q obstruction.

Together with the frozen 596 mixed origins, the independently rebuilt
compact cohort preserves the exact `650 = 596 + 54` outer partition.

## Exact q=0 source face

The 844 initial compact-q roots produce 844 unique physical 2D grazing
patches; there are no duplicate face representations.  Exact interval
root-order classification gives:

| q=0 face class | Patches |
|---|---:|
| excluded outgoing-chart mismatch | 20 |
| excluded unique-first owner mismatch | 628 |
| live frozen-stage-one chart match | 124 |
| unresolved multi-root | 48 |
| unresolved outgoing seam | 24 |

Thus 648 faces are excluded and 196 are nonexcluded.  Exactly 26 origins have
at least one nonexcluded q=0 patch; their key digest is
`8fd6d71bbc85a25fae10a8fa06cfe9bdb27b6b3e853c8b0f3ec88ff40fea3de5`.
The other 28 origins have every q=0 patch excluded; their key digest is
`875f2c7b746322af0f41125210f883f32fb887587fb05d4137d4927bd677df84`.

The first lexicographic nonexcluded q=0 witness is on origin
`W:N:03.15.11110101`, root
`W:N:03.15.11110101011010`.  It is `UNRESOLVED_MULTI` with active targets
`G[0,1]` and `W[-1,0]`.

## Half-open 2D/1D/0D ownership

All exact `t` and `s` endpoints within each origin/chart/sign group are used
to form an atomic source-face refinement.  Coincident 2D patches, atomic 1D
edges, and 0D corners are owned by the lexicographically least incident
source-root key.

| Stratum | Exact objects | Excluded | Live | Unresolved/conflict |
|---|---:|---:|---:|---:|
| 2D patch | 844 | 648 | 124 | 72 |
| 1D atomic edge | 2,218 | 1,666 | 326 | 226 |
| 0D atomic corner | 1,428 | 1,042 | 210 | 176 |

Owner-row digests are:

```text
2D  447b85624302b4190eef3459394333484324811e6ce8d959cac550ef75932125
1D  f1b8f8bb73b0b5d37dfb1672b541dbcce90ae4cfb834b93ec78c1170d3e206ea
0D  a11e8d55af56aa3df6d275592aab7f2eb5b1f32011a79f928a3be549e0a45914
```

These are source-stratum proof objects only.  None grants integer credit.

## Bounded depth-ten 3D q frontier

The deterministic q tree refines all 844 initial roots to at most ten extra
levels.  It gives:

| 3D class | Cells | Initial-root-equivalent volume |
|---|---:|---:|
| excluded outgoing mismatch | 5,610 | `5689/256` |
| excluded owner mismatch | 47,940 | `89203/128` |
| live frozen-stage-one chart match | 2,960 | `371/8` |
| residual multi-root | 71,876 | part of `20097/256` |
| residual outgoing seam | 8,512 | part of `20097/256` |

The exact coverage check is:

```text
184095/256 excluded
 11872/256 live
 20097/256 residual
216064/256 = 844 initial roots
```

There are 136,054 internal q-tree split faces with a unique half-open
lower-child owner and 136,898 terminal-or-residual 3D leaves.  Split-face
edge and corner counts are retained only as incidence ledgers; Round218 does
not claim a complete cross-root 3D/2D/1D/0D gluing.

No initial q root closes completely at depth ten.  All 54 origins have a
specific 3D obstruction.  The lexicographically first is:

```text
origin         W:N:03.15.01111111
root           W:N:03.15.01111111010010
q path         1101000101
extra depth    10
class          UNRESOLVED_MULTI
active targets G[0,1], W[-1,0]
```

For that origin, the maximally certified excluded q volume is `979/64` of
its 16 initial-root units, leaving exact residual `45/64`.

## Dimension-safe conclusion

Round218 grants zero whole-origin credit.  In particular:

- 21,334 child cells are not 21,334 records;
- exact q volume is not integer credit;
- a closed q=0 face is not a closed 3D source parent;
- a closed 2D patch, 1D edge, or 0D corner is not a whole origin;
- zero rectangular outer residual is not enough when the compact source
  stratum remains unresolved.

The source-W ledger therefore remains:

```text
74,584 excluded
 2,248 conservative live
76,832 total
252 remaining = 198 mixed + 54 compact-q
```

No global claim is promoted:

- `D02 = BLOCKED`;
- `D03 negative oracle = UNAUTHORIZED`;
- Gate5 remains `10/18`;
- complete global 18-field blocks remain `0`;
- `CM2 = NO-GO_FOR_CLAIM`.

## Next exact gate

The frontier separates the next work cleanly:

1. for the 28 origins whose q=0 faces are already all excluded, construct an
   analytic multi-root/first-order arrangement on the residual open 3D
   q-stratum; and
2. for the other 26, first resolve the 124 live and 72 unresolved q=0
   patches together with their atomic edge/corner ownership.

Blind subdivision beyond the frozen depth-ten tree is not a theorem and is
not used.  Whole-origin credit remains forbidden until the complete
cross-root 3D/2D/1D/0D partition is independently verified.
