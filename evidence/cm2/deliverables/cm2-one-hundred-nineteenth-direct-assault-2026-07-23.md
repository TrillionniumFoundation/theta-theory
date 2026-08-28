# CM2 one-hundred-nineteenth direct assault

Round119 installs a quantitative whole-trace C2/self-reach theorem for all
eight repaired source-grazing traces.

For source component `G`, with `R_G=9/25`, each individual trace now has
certified reach

```text
rho = 1/2500000000
```

in both extended/periodic ambient cylinders `(r,c)` and `(r,p)`, where
`r=(9/25)theta`.  The producer closes `29,992` adaptive base leaves,
`7,168` root leaves, and eight exact analytic base/root splices with zero
failed leaves.

The physical-state identity is exact: circle normalization, a unit
stereographic tangent, orthogonal reflection, and the planar Lagrange
identity give `c^2+p^2=1` on the base; the root has
`p=sigma0*sqrt(1-c^2)` on the same fixed branch.  Thus
`p_c=-c/p` and `p_cc=-1/p^3`.  The strict bounds

```text
theta_c > 2/5,
|p| > 1/51,
|r_cc| < 10800000,
|p_cc| < 132651
```

give common speed `m=18/125` and acceleration budget `A=11000000`.
The exact reach margins are

```text
m^2-A*rho  = 1021/62500,
m^2-4A*rho = 49/15625,
normal determinant lower bound = 1021/9000.
```

The double-minimizer proof includes interior/interior,
endpoint/interior, and endpoint/endpoint cases.  Angular span below `3/2`
also separates distinct periodic copies by more than `81/50`.

The independent 1024-bit verifier imports no Round119 producer or shared
Round119 mathematics helper.  It replays all `29,992+7,168` leaves and
independently dominates the producer's nine measured join lower bounds and
three measured join upper bounds.  Every ray passes the simultaneous
full-cover comparison at depth `1`, factor `2`, with `1024` join cells and
zero failed refinements.  A bounded depth-`1..3` attack ladder rejects all
`12/12` re-signed lower-inflation/upper-deflation mutants.  Together with
the static suite, `69/69` semantic attacks and `15/15` strict-JSON attacks
are rejected.

Dependency-residual widths between analytically identical formulae were
removed as acceptance gates.  An erroneous fixed source-chart radial-sign
guard was also removed: the legitimate base crosses the registered chart
seam.  Its replacement is the repaired chart/seam crosswalk, `local_x>0`
projective-lift control, strict physical path margins, and the exact analytic
join.  A re-signed `F_e x 2` mutant passes static checks but fails the actual
depth-`1`, depth-`2`, and depth-`3` dominance gates and reaches bounded
exhaustion.

Two independent full verifier replays and the canonical verification are
byte-identical.  Independent producer and seeded/locale replays are also
byte-identical to the canonical certificate.

The scope remains fail-closed.  This is per-trace extended-cylinder reach,
not reach of the eight-trace union.  It installs no uniform separation from
other singularities and no endpoint-inclusive two-sided collar in bounded
physical momentum space: at `c=0`, `p=+1` or `-1`.  No standard-curve child
or canonical recut is created.  Gate5 remains `10/18`, F1--F6 remain zero,
and CM2 remains `NO-GO_FOR_CLAIM`.

Final code/certificate bytes:

- producer `c384d1e3b67d4560e34de542637317e6ce9f84dcaa4b12f3fd8030ce646fc057`
- certificate `9ff985c91472e0ef57ced9fc10dbb6b2aa9e9627a5ac94c999caeefeca29a749`
- verifier `9749f5e15e0106f0a07c963e69bfaad75e65fc192a120c36d237687623d41ace`
- verification `c86d3694cd90c19c98f08965f0492f9f0ae41ed5f8fc272d393c9f64d1060cde`
