# CM2 Round 140 parent-W R1648 direct assault

Date: 2026-07-24

Strict verdict: **the final Round139 R1648 cell legally materializes one
source/path tuple, the fixed exact implicit leaf descriptor, the complete
rank-14 incidence path and `delta_14`, and prospective Round137-v1 contained
2D/1D witness ranks.  It still does not determine the larger component's
least rank or the oriented maximal leaf endpoint, so no historical
source-interval rank, natural short-cell `k`, parent-W ID, or restriction ID
is minted.**

## What survived assault

```text
source core:                        14
return depth:                       1648
official-word occurrences:         1648
unique official words:              141
incidence path:                   [14] x 1648
delta_14:                      1/8388608
2D contained level:                5883
1D contained level:                5883
```

The complete source/path tuple hash is

```text
5cec1061ec331e8f37929dfb1b2b2a78757309ba60198d571abd9e8cf6c70ed9
```

and the incidence-path hash is

```text
a2669f5587b2c7c10dc0d18fe1db2516df2b2049a7bf8cd37292636cd9c6fbe7
```

The contained rank decimal hashes are:

```text
2D  81ee4f795045d8478e621dbcaf2cba2437ccb168b34b770f995c012c0060927f
1D  fe02c53ca61c7ae9a81d189ffbf5d58cbae33ee16cb68e6248c65d5fc708c24d
```

The verifier proves these are least among Round137-v1 boxes/intervals
strictly contained in the particular Round139 inner rectangle/known leaf
subinterval.  It explicitly rejects the stronger statement that either is
the least rank somewhere in the larger connected object.

## Semantic and parser assault

The verifier re-signed and rejected 44 semantic mutations.  The targets
included:

- all three final Round139 pins;
- source core, return depth, path entries and path digest;
- fixed `s`, root uniqueness, and the enclosure/exact-real distinction;
- incidence entries, run-length encoding, `B`, and `delta_14`;
- both dyadic rows, rank encodings, locator caveats, and least-rank flags;
- every attempt to mint a historical component/interval rank or short-cell;
- parent-W/restriction/owner/t54/`q_j` and Gate5/CM2 promotions;
- missing or extra certificate fields.

It also rejected 16 malformed JSON cases: duplicate keys, finite/nonfinite
floats, negative-zero integers, BOM, invalid UTF-8, trailing data, a
top-level array, an unpaired surrogate, invalid integer/string encodings,
oversized integers, and an oversized document.

Seven in-process path-safety cases rejected missing, directory, symlink,
hardlink, FIFO, out-of-workspace, and oversized inputs.

## Hostile process/I/O assault

Thirteen isolated process cases all failed closed:

```text
Round140 producer byte drift
Round140 certificate byte drift
Round139 certificate byte drift
Round139 verifier byte drift
certificate symlink substitution
certificate hardlink substitution
dependency symlink substitution
dependency hardlink substitution
missing dependency
certificate replaced by directory
certificate replaced by FIFO
valid certificate supplied from an external path
verification output aliased to the certificate
```

The clean copied-directory producer replay and both hash-seed verifier
replays were byte-identical.  Total adversarial checks were:

```text
semantic mutations:                44/44 rejected
strict-JSON attacks:               16/16 rejected
in-process path attacks:            7/7 rejected
hostile process/I/O:               13/13 fail-closed
total:                             80/80
```

## Hard blocker that remains

Round35's natural `1e-90` cells are endpoint-anchored oriented arclength
cells on the maximal U-intersection leaf interval.  Round139 certifies only
a tiny interior leaf subinterval.  Its length being below `1e-90` does not
locate it relative to the endpoint-anchored grid.

Therefore all of the following remain null:

```text
historical Round27 component rank
historical Round27 c24-component ID
historical Round35 source-interval rank
historical Round35 natural short-cell k
historical Round35 source parent-W ID
historical Round35 image recut rank
historical Round35 rn-restriction ID
```

The final global verdict remains:

```text
Gate5 global maturity:           10/18
Gate5:                    NOT_CERTIFIED
CM2:                   NO-GO_FOR_CLAIM
```
