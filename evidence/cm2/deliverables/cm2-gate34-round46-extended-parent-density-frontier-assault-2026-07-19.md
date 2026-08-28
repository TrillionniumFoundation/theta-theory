# CM2 Gate 3/4 Round-46 extended-parent density assault

Date: 2026-07-19  
Verdict: **the extended pre-recut parent-bundle registry and its cross-cell
density/weight continuation are now numerical.  Gate 4 is reduced to a
target-sensitive covering weight and post-cut return.**

## 1. The missing bundle already exists before artificial recut

Every canonical source short cell lies on one regular owner/homogeneity
branch.  Its connected one-collision image exists before the deterministic
`10^-90` artificial recut.  Round 46 registers that image as

```text
extended-pre-recut-parent:
  (common-restriction-id)
  :(collision-time)
  :(physical-owner-homogeneity-child)
  :(image-parent-rank).
```

Its ordered children are precisely the artificial short cells.  Their
interiors are disjoint, their union is the complete image parent, and their
weights are restrictions of one pushforward conditional density rather than
independent family weights.  The registry is parameterized over every finite
regular arbitrary-`R_n` path and does not claim a finite enumeration.

This resolves the Round-45 registry and adjacent-weight typing gap.

## 2. Numerical cross-cell density continuation

On the source short cell, the frozen standard-density ratio is

```text
R_source < 2000/1999.
```

The source adapted length is at most `10^-90`.  The global one-step adapted
log-Jacobian `1/3`-distortion constant therefore gives

```text
osc(log J_*) < 1.5*10^25*(10^-90)^(1/3)
              = 3/200000.
```

Using `exp(x)<=1/(1-x)` gives the Jacobian ratio

```text
R_J < 200000/199997.
```

For the complete pre-recut image parent,

```text
rho_image(Tx)=rho_source(x)/J_*(x),
R_ext < R_source*R_J
      = 400000000/399794003.
```

No output-length factor appears: distortion is measured on the original
`10^-90` source cell before expansion.  This is exactly why the enormous
generic long-curve Hölder bound is unnecessary here.

## 3. Updated C24 covering threshold

Combining the new `R_ext` with the Round-45 crossing geometry gives

```text
mass(pair intersect C24)/mass(pair)
  > 399794003/1200000000000.
```

If crossing extended parents carry total family weight `beta` after a common
covering time, then the frozen C24 hit target follows from

```text
beta > 4608000/8167220347.
```

The reciprocal calibration remains sharp at the displayed integer scale:

```text
beta=1/1772 is safe,
beta=1/1773 fails.
```

## 4. Strict frontier

The following are still absent:

1. a uniform physical covering time `H_cover`;
2. a proof that C24-crossing extended parents carry
   `beta>4608000/8167220347` of every recovered proper family;
3. a numerical post-C24-cut return to the same proper class;
4. collision-time `C_fw/C_rev/q` and the strong cemetery.

Thus Gate 4 remains not certified.  Its first missing object is now purely
target-sensitive covering mass, not cross-cell density or registry typing.

