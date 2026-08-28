# CM2 Round 88 — Gate 3 finite-root collar extension

## Result

The Round-87 obstruction was a registry obstruction, not a dynamical one.
Exact recutting of the old positive/negative unions remains impossible, but an
explicit enlarged collar registry closes every finite `s=0` seam row.

- old certified positive-owner rows: `152/176`;
- newly closed positive-owner rows: `24/24`;
- newly closed negative-side rows: `24/24`;
- collar incidences: `48`;
- distinct physical collars after exact deduplication: `40`;
- selected contacts: `40` edge and `8` corner incidences;
- uniform rational `(t,p)` collar radius: `1/4096`;
- uniform rational two-sided `s` radius: `1/6400`;
- minimum strict margin from every collar to its source-core boundary:
  `7/102400`.

Thus the finite Round-69 root now has

```text
finite_root_local_two_sided_material_windows
  = 176/176_CERTIFIED_ON_ENLARGED_COLLAR_REGISTRY
```

## What was recertified

Each whole three-dimensional collar was checked at 512-bit Arb precision,
not merely at its center or on its former seam:

1. the collar lies strictly inside its pinned physical source core;
2. the complete parent-core first-owner proof is replayed;
3. the next collision has a strictly positive radicand;
4. the near flight time is strictly between zero and `tau_max`;
5. the landing chart and `(t,p)` coordinates lie strictly inside exactly the
   immutable destination core declared by the old row;
6. the collar has positive two-dimensional intersection with both contacting
   source rectangles.

The verifier independently repeats the geometry at 768 bits, reconstructs all
48 incidences and 40 unique collars, replays the 16 involved parent cores, and
rejects 7/7 semantic mutations, 15/15 coordinated pin mutations, and 4/4
strict-JSON attacks.

## Strict boundary of the conclusion

This repairs only the finite Round-69 `s=0` two-sided material-window field.
Gate 3 remains `NOT_CERTIFIED`: the result does not provide an all-cell or
all-depth common radius, a uniform Piola remainder, the global two-sided
trace/current atlas, a stopped `MT_DQ` estimate, or a global strong recipient.
The Round-87 no-recut theorem is preserved verbatim for the old immutable
registry; Round 88 succeeds by explicitly adding positive-width collars.

