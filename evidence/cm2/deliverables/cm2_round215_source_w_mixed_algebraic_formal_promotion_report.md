# CM2 Round215 — formal source-W mixed-algebraic promotion

Date: 2026-07-27  
Verdict: `PARTIAL_FORMAL_SOURCE_W_MIXED_ALGEBRAIC_PROMOTION__D02_STILL_BLOCKED`

## Result

Round215 performs an outcome-blind scan of the complete frozen Round201
source-W registry and formally promotes exactly two complete original
physical source parents:

```text
W:N:06.00.01111000
W:S:H.06.00.01111000
```

Their ordered-key digest is
`f7c3a8854d6b7b561f1bb90dac18ebf7551f5ff4be1a73af764846808fbf5941`.
Both belong to the frozen `DELTA_H_OR_MULTI_NO_Q` class.  Selection occurs
only after the full 198-origin strict-interior active cohort and all 18,432
residual cells have been analyzed.

The frozen registry partition is independently reconstructed as:

```text
596 outcome-blind source-W priority origins
200 Round201-incomplete origins
  2 Round212 retained source-seam origins
198 strict-source-interior active mixed origins
 54 separate compact-q origins
```

The two Round212 seams are never injected into the active cohort, and the 54
compact-q origins are audited separately.  Of the 198 active mixed origins,
two are now complete and 196 remain blocked; together with the two retained
seams, the remaining mixed count is 198.

## Whole-origin proof

Each promoted parent is covered by exactly 638 excluded closed 3D leaves:

| Proof source per origin | Leaves |
|---|---:|
| Pinned pre-depth-14 Round176 terminals | 5 |
| Pinned Round176 preclosed frontier | 5 |
| Pinned Round180 inherited terminals | 116 |
| Pinned Round201 exact-behind cells | 504 |
| New Round215 strict closed boxes | 8 |
| **Total** | **638** |

The Round176 replay gives 57 frontier pieces per origin: five already closed
and 52 residual roots.  Its five earlier terminal leaves are rebuilt
independently rather than inferred from a prior ledger boolean.  The exact
prior coverage numerator is `7/64` per origin.  Round180 then reconstructs
116 inherited excluded terminals and 512 final cells.  Of those final cells,
504 are closed by the pinned Round201 exact-behind theorem and the remaining
eight are closed by Round215.

For every new cell, exact Arb interval evaluation proves:

- `dDelta/dp` has one strict sign on the whole closed box;
- both `p`-endpoint values of `Delta` are strictly positive;
- therefore the `Delta=0` graph does not meet the closed box;
- enhanced root order has a unique first target;
- that target's owner differs from the frozen source chart; and
- the exclusion restricts to all owned faces, edges, and vertices.

The unique first target is `G[1,1]` for the `W:N` parent and `G[1,0]` for the
`W:S` parent.  Because owner mismatch already excludes the complete box, the
eight outgoing-owner margins are correctly marked not applicable for these
16 cells.  A distinct active-census control cell,
`W:N:06.00.011001100110010100`, supplies a deterministic case in which all
eight outgoing margins are strict; its fixture digest is
`0ef96424d9a009ea1a381049e1d5e20444289af2da81603f2b6c88908a7e0522`.

No child count, rational volume, sheet, edge, corner, seam, or compact-q cell
is converted into integer credit.  Each credit represents one complete
original chart-owned physical 3D source parent.

## Independent lower-dimensional ownership

The certificate does not rely on a legacy conclusion boolean.  For each
candidate, it explicitly rebuilds:

| Owner class per origin | 2D | 1D | 0D |
|---|---:|---:|---:|
| Round176 internal split strata | 61 | 174 | 124 |
| Round180 internal split strata | 576 | 1,525 | 966 |
| Original-parent outer strata | 6 | 12 | 8 |

Internal equalities belong to the lexicographically least lower child and are
recursively reduced to exact terminal descendants.  Parent outer faces,
edges, and corners use the unique half-open parent-side leaf partition.
Internal and outer classes are disjoint, every owner row has exact measure
coverage, and every row reduces to an excluded closed 3D enclosure.

The certificate records
`trusted_legacy_ledger_conclusion_boolean = false`.  Thus a stale upstream
`true` value cannot substitute for the rebuilt 3D/2D/1D/0D partition.

## Full-census non-promotion

The full active mixed analysis contains:

| Item | Exact value |
|---|---:|
| Active origins | 198 |
| Residual cells | 18,432 |
| Analytically closed cells | 3,444 |
| Still-blocked cells | 14,988 |
| Active exact volume | `1593/204800000` |
| Analytically closed exact volume | `152397/104857600000` |
| Blocked exact volume | `663219/104857600000` |

The blocked-cell partition is:

```text
12,888 clipped-endpoint overwrap
 1,176 multiple-Delta obstruction
   816 no-unresolved-unique-first obstruction
    60 full-Delta negative-side not excluded
    48 genuinely live
14,988 total
```

The two promoted origins are the only complete whole origins.  The other 196
active origins and both retained seams receive zero credit.

The separate compact-q outer audit remains:

```text
54 origins
21,334 children
18,782 geometrically closed
 2,552 geometric residual
35,852 deleted candidates
 3,692 failed candidates
```

The global 650-origin conservation is also rebuilt:

```text
182,776 children
161,648 geometrically closed
 21,128 geometric residual
233,356 deleted candidates
 22,580 failed candidates
```

These counts are conservation evidence only.  They grant no compact-q or
whole-origin credit.

## Integer ledger

Round215 changes only the conservative source-W whole-origin ledger:

```text
74,582 + 2 = 74,584 excluded
 2,250 - 2 =  2,248 conservative live
74,584 + 2,248 = 76,832
```

The exact remaining priority partition is:

```text
198 incomplete mixed origins
 54 compact-q origins
252 remaining priority origins
```

## Independent verification and attacks

The verifier pins both the formal producer and bounded probe as inert bytes
and does not import or execute either one.  Before reading the certificate it
independently reconstructs the complete `596 -> 200 -> 2 + 198` registry,
18,432-cell active analysis, 54-origin compact outer audit, 650-origin global
conservation, both promoted candidates, all 1,276 candidate closed leaves,
and every lower-dimensional owner reduction.

The official verification is `PASS_PARTIAL_FORMAL_ROUND215`:

- certificate result SHA256:
  `39d38cda12566e25b341b861e0e1ee379138aa465424254a6b60ea35da5629ee`;
- verification result SHA256:
  `f6fd2b6927d003f216dac1caf24452149283286227475cab423aa8fde77e960d`;
- genuinely re-signed semantic attacks rejected: `24/24`;
- strict JSON/encoding attacks rejected: `13/13`;
- lexical and parent-symlink path attacks rejected: `18/18`;
- producer output-path attacks rejected: `6/6`;
- actual hostile input objects rejected: `7/7`; and
- actual hostile output objects rejected: `4/4`.

Every semantic mutation is re-signed with the digest of the mutated result
and then passed through the same official certificate-verification entry
point.  Rejections therefore establish full expected Python-object and
canonical-byte equality rather than merely detecting a stale signature.

The semantic suite covers candidate substitution/omission, seam or compact-q
injection, cell and endpoint-sign rewrites, inherited and prior-leaf
corruption, lower-stratum restriction and owner-count/hash corruption,
legacy-ledger trust injection, outer/internal owner confusion, the eight
margin control, active/global census rewrites, ledger inflation, and a false
D02 promotion.

The filesystem suite exercises real symlink, hardlink, FIFO, directory,
empty, oversized, and missing objects.  Temporary objects are cleaned and no
protected artifact is modified.

The verifier reimplements the bounded-probe mathematics and formal
composition, but exact AST comparison finds substantial shared function-body
structure.  No implementation-diverse claim is made.

## Fail-closed development history

An early formal attempt correctly failed because the pre-depth-14 Round176
terminal leaves were absent from the proposed parent/outer owner map.  The
observed outer-face coverage was `3/102400`, short of the required
`1/25600`.  The proof was repaired by independently replaying the Round176
binary tree and obtaining exact prior coverage `7/64`; no theorem flag or
coverage requirement was weakened.

An initial verifier run was stopped after its hostile cases were found to
compare only a mutated canonical document.  The final verifier re-signs every
mutation and routes it through the official entry point.

## Global state and next source-W gate

Round215 makes no global promotion:

- `D02 = BLOCKED`;
- `D03 negative oracle = UNAUTHORIZED`;
- Gate5 remains `10/18`;
- complete global 18-field blocks remain `0`;
- `CM2 = NO-GO_FOR_CLAIM`.

The next source-W core gate is the frozen 54-origin compact-q cohort.  It must
rebuild the complete 3D/2D/1D/0D half-open source-stratum owner partition,
exact first-root/order evidence, and endpoint/corner ownership.  A compact-q
cell, volume, face, edge, or point is never a whole-origin credit.
