# CM2 Round180 — full multi-residual dimension-safe bounded pass

Date: 2026-07-26

## Verdict

`PASS_PARTIAL_BOUNDED_ROUND180`.

Round180 processes every one of the 44,040 source-W multi-candidate residual
cells frozen by Round176 and independently validates exactly 32 additional
whole original physical-parent exclusions.  The conservative source-W ledger
is therefore

```
73,392 excluded + 3,440 live = 76,832 refined source-W records.
```

This is a bounded ledger improvement, not a core-gate closure.  D02 remains
`BLOCKED`, D03 remains unauthorized, Gate5 remains `10/18`, the global
complete 18-field-block count remains zero, and CM2 remains
`NO-GO_FOR_CLAIM`.

## Complete residual input

Round180 starts from the pinned Round176 residual ledger:

| Residual category | Depth-14 cells |
|---|---:|
| clipped/face-overwrap single discriminant graph | 26,728 |
| multi-discriminant, two to five targets | 10,802 |
| full-p discriminant graph requiring first-root equality | 4,812 |
| source-grazing compact-q residual | 1,478 |
| typed tangency plus outgoing-seam double graph | 220 |
| **Total** | **44,040** |

Those cells belong to 2,162 original depth-8 parents.  Exactly 686 parents
already contain a strict `LIVE` or `MIXED` witness and therefore cannot receive
whole-parent exclusion credit.  The remaining 1,476 are only exclusion upper
bound candidates; the upper-bound partition is

```
1,476 = 32 newly certified + 1,444 still open.
```

The exact 686-key digest is
`1d974a10739e6e2dc1a99b9a8eec721fe70d1bf7fc92e6d7c283d1aea00769f5`.
The exact 1,476-key digest is
`c15ab39fcffba53204de689f631110e5888df616e47d56a08f8cb42f72ee8aad`.

## Bounded rectangular refinement

The pass evaluates 755,544 tree nodes.  Its closed terminal census is:

| Disposition | Child cells |
|---|---:|
| excluded | 87,730 |
| live | 11,138 |
| mixed/analytic | 996 |

The closure methods are 76,500 direct strict boxes, 18,676 same-sign monotone
Delta boxes, 2,228 outgoing-H rectangle-tree cells, and 2,460 typed Delta
three-stratum cells.

Four origins become completely replaced but remain nonexcluded:

```
W:E:00.14.10100011
W:E:01.13.01010010
W:E:06.02.10101101
W:E:07.01.01011100
```

Their digest is
`cf1458e835fc80e4aaf695d8144ce32dcf0bece45a11cc15b22a4e9327b4fb26`.

After the bounded pass, 2,126 original parents still carry residual cells.
The 299,928 child-residual count is a refinement diagnostic, not an integer
record count:

| Residual category | Child cells |
|---|---:|
| clipped/face-overwrap | 185,438 |
| root equality | 53,144 |
| multi-Delta | 54,214 |
| compact-q grazing | 6,838 |
| typed double graph | 294 |

## The 32 whole-parent exclusions

The exact 32-key digest is
`70300cade4136fdb41f4b1f8900b47b89f0d9a498f7afd0c0d614296f84b3c87`.
The per-origin summaries digest is
`57ebdfe74be4c911ebe86c15a63308f045c81013e47a01cf0aac52c43170ca1d`.

Two depth summaries are deliberately kept separate:

| Summary | Counts |
|---|---|
| earliest actual completion | depth 1: 18; depth 3: 8; depth 4: 6 |
| closed-by tranche cutoffs | depth 2: 18; depth 3: 8; depth 4: 6 |

The proof-route partition is:

| Route | Origins | Exact-key digest |
|---|---:|---|
| pure direct | 18 | `d53c2ea7918a3e20547b89d1147a66cff93d1b33cb59c42df17aaf643a59ef48` |
| pure same-sign Delta | 6 | `5399d4e78f1a2291aa724e6ec71c08b30cab486b37ba7323853f63a4cbd70b5e` |
| mixed direct and same-sign Delta | 8 | `a6f5791034f312d2ef03fbecea6076184684736ed83541d2fa6cce7633dd7a84` |

All 32 origins are strictly inside the physical source chart.  Every credited
origin has a complete 3D, 2D, deduplicated 1D, and 0D ledger.  Internal
analytic strata, child counts, rational volumes, source-chart guard regions,
and compact-q volumes contribute no integer record credit.

## Required nonclosure regressions

The outgoing-H regression remains open:

```
origin: W:N:04.00.10000000
cell:   W:N:04.00.1000000000010110
t:      [2301/25600, 5841/64000]
p:      [-1, -1023/1024]
s:      [1/800, 1/400]
```

Its depth-at-most-four tree contains four typed seam composites and four
strict live rectangles, at depths `{3: 7, 4: 1}`.  Its H-zero graph is 2D,
pairwise intersections are at most 1D, triples/corners are at most 0D, and its
whole-parent credit is zero.  Round176's local H closure is not generalized.

The compact-q depth-10 profile also remains nonclosing for all 1,478 inputs:

| Class | Cells |
|---|---:|
| terminal outgoing mismatch | 15,586 |
| terminal owner mismatch | 57,612 |
| terminal live | 19,778 |
| residual multi | 115,456 |
| residual outgoing seam | 22,976 |

The residual total is 138,432 q-cells, or exactly `2163/16` in depth-14
parent-equivalent volume.  The `r=0` grazing face is a 2D stratum; its
intersections are lower-dimensional.  Whole-origin integer credit is zero.

## Producer output safety

The final producer uses same-directory `mkstemp + fsync + os.replace`.
It accepts only:

- the one official Round180 certificate path; or
- a hidden `.cm2_round180_*_certificate.json` path in the deliverables
  directory for an explicitly requested cold replay.

The producer itself, all seven Round176 pins, and the five Round180
non-certificate artifact paths are protected.  Existing targets must be
regular, non-symlink, and single-link files.  Ordinary same-directory regular
outputs are not implicitly caller-authorized.

The producer's 19 path attacks reject symlink and hardlink outputs, parent and
nested-directory escapes, existing-directory and FIFO targets, and temporary
protected fixtures for every protected logical path.  Real pins are used only
for protection-set membership checks; write attempts against real pins are
zero.

The earlier pre-guard producer/certificate hashes are superseded and carry no
Round180 authority.

## Independent verification

The verifier does not import or execute the Round180 producer.  Relative to
the frozen, independently verified Round176 geometry it reconstructs:

- all 44,040 residual cells and all 2,162 residual origins;
- both bounded refinement depths and all 32 whole-parent coverage trees;
- every credited 3D/2D/1D/0D ledger;
- the H eight-piece nonclosure regression;
- the complete compact-q depth-10 profile;
- the producer output-safety contract and all 19 stable attack labels; and
- the complete expected certificate result with canonical equality.

Attack results:

| Suite | Rejected |
|---|---:|
| re-signed semantic mutations | 178/178 |
| per-origin method/coverage/strata/physical mutations | 128/128 |
| strict JSON attacks | 9/9 |
| verifier path-safety attacks | 7/7 |

Every semantic mutation is re-signed and checked with the frozen result-digest
shortcut disabled.

Producer runs under `PYTHONHASHSEED=18021` and `18022` are byte-identical.
Verifier runs under `18031` and `18032` are byte-identical.  A parent cold
replay under seed `180051` is also byte-identical to the official
verification.

## Next core work

Round184 begins from the exact 1,444 still-open exclusion upper candidates.
Before attempting closure it will publish a reconstructible, stable ordering
by residual-category support, child count, and exact origin-key tie-break.
The first tranche is restricted to pure single clipped-Delta candidates, with
explicit `Delta<0`, `Delta=0`, and `Delta>0` cells, frozen owner and outgoing
chart recomputed on the graph, and half-open split-face ownership deduplicated.

Later tranches proceed through root-equality, Delta-H/multi, and compact-q.
Only complete 3D/2D/1D/0D whole-parent closures may change the integer ledger.
