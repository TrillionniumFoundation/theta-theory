# CM2 Round176 — dimension-safe multi-origin whole-parent exclusion

Date: 2026-07-26

## Verdict

`PASS`, limited to the pinned source-W frozen-prefix stage-one ledger.

Round176 independently validates exactly 182 whole original depth-8
multi-candidate parent exclusions.  Together with the independently verified
Round175 tangency ledger, the new conservative composition is

```
73,360 excluded + 3,472 live = 76,832 refined source-W records.
```

D02 remains `BLOCKED`, D03 remains unauthorized, Gate5 remains `10/18`,
the global complete 18-field-block count remains zero, and CM2 remains
`NO-GO_FOR_CLAIM`.

## Independent reconstruction

The verifier imports only
`cm2_gate3_candidate_first_hit_cert.py`.  It does not import or execute the
Round165, Round166, Round170, or Round176 producer code.

Starting from the pinned Gate3 candidate and target geometry, it reconstructs:

| Layer | Exact census |
|---|---:|
| owner-active depth-8 multi parents | 2,616 |
| evaluated depth-8-to-14 tree nodes | 167,984 |
| evaluated target records | 415,570 |
| depth-14 frontier cells | 56,780 |
| frontier closed excluded | 6,250 |
| frontier closed live | 3,590 |
| frontier closed mixed/analytic | 2,900 |
| frontier residual | 44,040 |
| fully replaced original parents | 454 |
| whole-origin excluded | 182 |
| whole-origin live | 236 |
| resolved mixed/analytic | 36 |

The independently reconstructed 182-key digest is
`bfb29d76ced106a3d69a3d4c1ebb2271c45a1567197a3e7da93e883cae6c91b3`.
Its set difference from the Round170 candidate set is empty.  Round170's
candidate digest is not accepted as a source of truth.

## The 164/18 risk split

The 182 promoted parents are not treated as one homogeneous aggregate:

| Proof route | Origin parents | Closed frontier cells |
|---|---:|---:|
| prior strict terminal cells alone | 164 | 0 new analytic closures |
| outgoing-H closed rectangles | 8 | 60 |
| same-sign monotone Delta rectangles | 8 | 14 |
| typed Delta three-stratum partitions | 2 | 32 |

The 18 analytic origins are:

### Outgoing-H closed rectangles

```
W:E:01.13.00111010
W:E:01.13.10001000
W:E:02.12.00010110
W:E:05.03.11101001
W:E:06.02.01110111
W:E:06.02.11000101
W:N:07.02.10100001
W:S:H.07.02.10100001
```

### Same-sign monotone Delta rectangles

```
W:E:03.10.10000011
W:E:04.05.01111100
W:N:00.13.10100101
W:N:00.14.11111110
W:N:05.15.01011100
W:S:H.00.13.10100101
W:S:H.00.14.11111110
W:S:H.05.15.01011100
```

### Typed Delta three-stratum partitions

```
W:N:03.15.01011111
W:S:H.03.15.01011111
```

Every one of these 18 origin rows is separately covered by three re-signed
semantic attacks: method, required-dimensional-strata ledger, and coverage.
That contributes 54 of the verifier's 95 semantic mutation attacks.

## Dimension and ownership rules

Integer credit is attached only to a completely replaced original physical
depth-8 parent.  Child counts and rational volumes are not converted into
integer record credit.

The verifier reconstructs and enforces:

- all closed 3D dyadic descendants;
- the `Delta<0`, `Delta=0`, and `Delta>0` partition, with the zero graph
  recorded as 2D;
- graph edges as 1D and graph corners as 0D;
- all closed split faces and their lower-dimensional intersections;
- lower-child ownership of each equality split face, recursively and
  lexicographically for multiple equalities;
- strict closed-box exclusions inheriting to the owned boundary faces;
- the compact-q `r>0` / `r=0` dimensional split for the independently replayed
  grazing frontier, although no compact-q origin contributes to the 182
  promoted parents.

The two typed-Delta origins contribute 32 two-dimensional Delta graphs,
128 graph edges and 128 graph corners in their per-box ledger, and no
graph-only integer credit.

## Physical source-chart guard

The source-chart equation is handled separately from collision geometry:

```
physical interior: 2*t^2 < 1
source seam:       2*t^2 = 1
rational guard:   2*t^2 > 1
```

Among the 182 credited origins, 180 are strictly inside the physical chart.
Exactly two cross the physical seam:

```
W:E:00.15.00000100
W:E:07.00.11111011
```

The E chart owns the half-open source seam.  The rational guard portion has
zero exterior-exclusion credit and is not added to the integer ledger.

## Round175 composition

The Round175 producer, certificate, verifier, verification result, report, and
manifest are hash-pinned and the manifest entries are replayed.  Its six new
tangency-parent exclusions combine with the ten Round172 exclusions into 16
cumulative tangency keys.

Those 16 tangency keys and the 182 Round176 owner-active multi-candidate keys
have empty exact-key intersection.  Therefore the composition is:

| Ledger | Excluded | Conservative live |
|---|---:|---:|
| Round175 base | 73,178 | 3,654 |
| Round176 delta | +182 | -182 |
| Combined | 73,360 | 3,472 |

## Verifier hardening

The verifier rebuilds the complete expected certificate result and requires
full canonical equality.  It also verifies recursive exact-key layer digests
for the 2,616 origins, all 56,780 frontier cells, the three closed classes,
the 44,040 residual cells, and all three fully-replaced-origin classes.

Attack results:

| Suite | Rejected |
|---|---:|
| re-signed semantic mutations | 95/95 |
| strict JSON attacks | 9/9 |
| path-safety attacks | 7/7 |

Producer and verifier cold replays under two distinct `PYTHONHASHSEED` values
are byte-identical.

## Remaining core work

Round176 leaves 2,434 original multi-candidate parents without whole-parent
credit.  The next bounded work is the unresolved multi-Delta, full/clipped
Delta, root-equality, tangency/seam double-graph, compact-q, and
clipped/face-overwrap arrangements.  No D02 or Gate5 promotion follows from
this round.
