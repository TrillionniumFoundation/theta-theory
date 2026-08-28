# CM2 Gate 3/4 Round-45 parent-bundle cross-cell frontier assault

Date: 2026-07-19  
Verdict: **the Round-44 phrase “long canonical parent-`W`” is corrected at
the exact registry scale.  A single canonical short-cell ID cannot cross the
fixed inner C24 strip; the missing numerical object is an extended pre-recut
parent bundle with adjacent-cell density and family-weight continuation.**

## 1. Exact scale correction

The frozen canonical parent-`W` registry cuts every natural ID into Euclidean
arclength cells of length at most

```text
10^(-90).
```

Use the fixed inner strip

```text
chart G:E,
t in [11/1000,19/1000],
p in [-1/1000,1/1000].
```

Its closure lies inside the frozen bump support and one C24 axis core.  A
connected transverse graph crossing the two `p` endpoints has

```text
Delta phi = 2 asin(1/1000) > 1/500,
Euclidean arclength > 1/500.
```

Therefore one crossing uses strictly more than `2*10^87` canonical cells;
the exact minimum integer allowed by the frozen upper cell length is

```text
2*10^87 + 1.
```

Consequently, no single canonical short-cell ID can be the “long parent” on
which Round 44 proposed a direct covering/minorization.

## 2. Why the current cellwise facts do not bridge the gap

The existing per-cell density ratio `2000/1999` and proper-family bound do not
compare the family weights of adjacent short-cell IDs.  An exact logical
countermodel places all mass on one avoiding cell of an abstract ordered
extended parent while the geometric union of all cells crosses C24.  Every
occupied cell has constant density and the family remains proper, yet its C24
hit mass is zero.

This is a nonimplication model for the current certified premises, not a
counterexample to the physical billiard.  It proves that cellwise properness
cannot be substituted for cross-cell weight continuation.

## 3. Exact sufficient interface

Introduce one same-ID extended pre-recut pair, and certify

```text
max rho_extended / min rho_extended <= R_ext
```

across the entire joined pair.  A monotone extended pair has total Euclidean
graph length `<6`.  Since its C24 crossing segment has length `>1/500`, one
crossing pair satisfies

```text
mass(pair intersect C24) / mass(pair) > 1/(3000 R_ext).
```

If, after `H_cover` collisions, crossing pairs carry family weight at least
`beta`, then

```text
mass(C24) / mass(G) > beta/(3000 R_ext).
```

To reach the already frozen target

```text
epsilon_hit = 21/111718750,
```

it is sufficient to prove

```text
beta > 3000 R_ext * 21/111718750.
```

Only as a hypothetical numerical calibration, if the unavailable extended
ratio happened to equal `2000/1999`, then one pair would contribute more than
`1999/6000000`, and it would suffice to have

```text
beta > 4032/7146425.
```

Here `1/1772` is safe while `1/1773` fails.  This calculation does not certify
`R_ext=2000/1999`.

## 4. Strict frontier

The following remain unproved and numerical:

1. an extended pre-recut parent-bundle ID joining consecutive artificial
   short cells;
2. its cross-cell density/weight continuation constant `R_ext`;
3. a uniform covering time `H_cover` and crossing-family weight `beta`;
4. the post-C24-cut return to the same proper class;
5. collision-time `C_fw/C_rev/q` and the strong cemetery.

Thus Gate 4 remains not certified.  The correction removes an ill-typed
single-cell route while leaving a precise and testable extended-bundle route.

