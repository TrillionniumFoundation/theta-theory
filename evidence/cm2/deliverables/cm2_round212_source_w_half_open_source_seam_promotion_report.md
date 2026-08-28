# CM2 Round212 — formal source-W half-open source-seam promotion

Date: 2026-07-27  
Verdict: `PARTIAL_FORMAL_SOURCE_W_HALF_OPEN_SOURCE_SEAM_PROMOTION__D02_STILL_BLOCKED`

## Result

Round212 closes the source-domain bookkeeping that Round184 and Round201
conservatively held at zero.  It scans the complete Round201 upper-candidate
set and independently finds exactly 26 rational source boxes crossing the
physical diagonal `2*t^2=1`.

The exact outcome is:

- 24 origins have complete excluded inherited and final target partitions
  and receive one whole-origin credit each;
- 2 origins remain target-incomplete and receive zero credit;
- promoted classes: 18 `PURE_SINGLE_CLIPPED_DELTA` and 6
  `DELTA_H_OR_MULTI_NO_Q`;
- retained incomplete classes: 2 `DELTA_H_OR_MULTI_NO_Q`.

The complete 26-key digest is
`ed624beb47da60b591ae1f60086677ebecfdacb4da63cece4a8969680f22c31b`.
The promoted 24-key digest is
`74bc6aba8c3eebc4ca276a87036c9752e1356da9ead8b66241dda6b09f842554`.

The two retained origins are:

```text
W:N:07.00.11111011
W:S:H.07.00.11111011
```

Each has 144 final cells: 72 strict owner-mismatch exclusions and 72
`UNRESOLVED`.  Round212 neither drops those `2 × 72` residual cells nor
promotes either origin.

## Rebuilt target evidence

The targeted replay starts from all 1,476 source-W upper candidates and
rebuilds only the 26 source-seam composites.  It replays:

- 3,666 Round180 final cells;
- 1,630 inherited terminals;
- 6,832 target proof objects after the bounded pure-target depth-two
  refinement;
- exact inherited/final volume conservation for every origin;
- all owned split faces and inherited 3D/2D/1D/0D exclusion semantics.

No child count, rational volume, source seam, guard slice, or lower-dimensional
stratum is converted into integer credit.  A credit is issued only when the
complete original chart-owned physical source parent has a complete excluded
target partition.

## Exact half-open source partition

Every selected rational source interval contains exactly one algebraic root
`t=±1/sqrt(2)`, proved by exact rational endpoint-square inequalities.  Each
box is partitioned into:

1. the open chart interior `2*t^2<1`;
2. the two-dimensional diagonal `2*t^2=1`; and
3. the open guard/recoordination slice `2*t^2>1`.

The horizontal `E/W` family owns the equality; the vertical `N/S` family
excludes it.  The guard slice is re-coordinated by

```text
t_adj = ±sqrt(1-t_source^2)
p_adj = p_source
s_adj = s_source
```

with exact Jacobian `±t_source/sqrt(1-t_source^2)`, strictly nonzero on every
open guard slice and equal to `±1` on the selected seam.  The transformation
preserves the physical normal, source position, velocity, and `s`.

The promoted census is:

| Item | Exact count |
|---|---:|
| Original charts `E / N / S` | `6 / 9 / 9` |
| Source signs negative / positive | `15 / 9` |
| Half-open seam owners `E / W` | `12 / 12` |
| Guard adjacent charts `W / E / N / S` | `12 / 6 / 3 / 3` |

The sign census is intentionally `15/9`, not a presumed symmetric `12/12`;
it follows the exact ordered 24-key set.

All seams and open guard slices are counted once.  Guard-outside exterior
credit and separate source-seam integer credit are both zero.

## Integer ledger

Round212 changes only the conservative source-W whole-origin ledger:

```text
74,558 + 24 = 74,582 excluded
 2,274 - 24 =  2,250 conservative live
74,582 + 2,250 = 76,832
```

The exact remaining priority partition is:

```text
200 incomplete mixed origins
 54 compact-q origins
254 remaining priority origins
```

The two target-incomplete source-seam origins are members of the 200
incomplete mixed origins, not an additional residual class.

## Independent verification and attacks

The verifier pins the producer as inert bytes and never imports or executes
it.  Before loading the certificate it independently reconstructs all 26
seam facts, the exact 24/2 partition, both 72-cell unresolved sets, all
per-origin target summaries, each source transfer, and the final ledger.

The official verification is `PASS_FORMAL_ROUND212`:

- certificate result SHA256:
  `a4e6e44aa55eedd376f5dd5d01a82f5c8dfae19ebb433dfb0017d07718004c7d`;
- verification result SHA256:
  `5ab0bb7fa213fa0e86c1252dad1a21b96ab54d4b48025e767c8af7a953383d2e`;
- re-signed semantic attacks rejected: `14/14`;
- strict JSON attacks rejected: `8/8`;
- path/type/output attacks rejected: `10/10`.

The semantic suite covers promoting a 72-unresolved residual, duplicating or
omitting promoted keys, forging `74582/2250`, changing half-open ownership or
the adjacent chart, zeroing the rechart Jacobian, granting guard or seam
credit, dropping either residual's unresolved cells, forging the remaining
priority count, and promoting D02.  Row and ledger digests are recomputed for
the row-level attacks.

The path suite performs real symlink, hardlink, directory, and FIFO probes and
also rejects nested output, parent escape, symlink-parent alias, and protected
producer/certificate/upstream-verifier outputs.  No protected artifact is
modified.

The verifier shares the pinned Round201 low-level target kernels; it is not
claimed to be an implementation-diverse second derivation of collision
geometry.  Its source-domain partition and certificate validation are
independently implemented.

## Global state and next source-W gate

Round212 makes no global promotion:

- `D02 = BLOCKED`;
- `D03 negative oracle = UNAUTHORIZED`;
- Gate5 remains `10/18`;
- complete global 18-field blocks remain `0`;
- `CM2 = NO-GO_FOR_CLAIM`.

The next source-W core gate is dimension-safe treatment of the remaining 200
incomplete mixed origins, beginning with their unresolved Delta/root-order
sheets and all required 2D/1D/0D glue.  The 54 compact-q origins remain a
separate source-grazing stratum.  No point, sub-box, sheet, or low-dimensional
count may be promoted as a whole-origin credit.
