# CM2 Round 72 — full base-fibre R1 family atlas and local numeric fields

Date: 2026-07-21  
Scope: append-only continuation from Round 71  
Strict verdict: **All 1,152 frozen terminal-core-preimage families are now
classified at `s=0`: exactly 32 are nonempty and 1,120 are empty.  The 32
positive families are unique connected clipped components and receive numeric
F10, F13 and F16 rows.  This closes the finite base-fibre terminal-preimage
subatlas, not the all-depth physical atlas or any composite gate; CM2 remains
`NO-GO_FOR_CLAIM`.**

## 1. Exhaustive 1,152-family classification

A shared Arb interval tree evaluates the actual one-step collision map once
per source box and simultaneously tests all compatible destination-core faces.
The exclusion grammar contains the destination chart sign, the face level and
the other face coordinate.  This chart-sign clause is essential: omitting it
confuses the N/S or E/W semicircles that share one scalar chart coordinate.

The final tree has

```text
24 source cores,
824 interval map tests,
424 prefix-complete leaves,
maximum depth 13,
32 positive family IDs,
1120 certified-empty family IDs,
0 unresolved families.
```

The sorted union of the positive and empty IDs has SHA-256
`feaf1a97c8b746596b5fb46b23a6de59a5d381d0648095b5c14b6d9071905b8b`,
exactly the frozen 1,152-family registry digest.  No candidate family is lost,
duplicated or left as a corner residual.

## 2. Full clipped connected components

For every one of the 16 positive source cores, a second Arb tree certifies the
signs of

```text
d_t(target t), d_p(target t),
d_t(target p), d_p(target p),
det D_(t,p)(target t,target p)
```

on the whole source core.  It uses 112 tests, 64 prefix-complete leaves and
maximum depth two.  On every positive face, the level is strictly monotone in
source `p`, while the two-coordinate Jacobian never vanishes.  Hence the level
is a unique graph and the other target coordinate is strictly monotone along
it.  Clipping by the source and destination intervals produces exactly one
connected component, assigned rank zero.  Thus the 32 Round-71 local germs
extend to the 32 full clipped components; multiple-component ambiguity is
removed.

## 3. Numeric F10, F13 and F16

Each component receives a canonical compact parameter germ with radii

```text
delta_t=1/10^10,
delta_p=1/10^6,
delta_s=1/10^10.
```

Second-order Arb jets of the physical level equation certify the `p` bracket,
`F_p != 0`, the implicit derivatives `p_t,p_s,p_ts,p_ss`, and the collision
current density

```text
rho=(R_source/sqrt(1-t^2))*p_s.
```

All 32 F10 searches therefore terminate with explicit integers:

```text
minimum N_F10 = 3,
maximum N_F10 = 39,
sum N_F10 over 32 components = 480.
```

Every face has F13 current variation strictly below `1/10^9`; the 32-face
total is below `4/125000000`.  Exact area-preserving Piola transport gives the
same `4/125000000` upper for the corresponding local F16 flux costs.

## 4. Strict boundary

- The 96 stationary source-core faces remain separately materialized; a shared
  face subdivision/incidence quotient is not assembled here.
- The result is for the base fibre and one-step terminal-core preimages.  It is
  not an arbitrary-depth `R_n` face atlas or a limiting rank/path sum.
- F14, F15, F17 and F18 remain open; the common anisotropic recipient and
  cemetery-compatible all-input bounds are absent.
- Gates 1--4 still lack the stable/material same-key crosswalk and all-depth
  commuting-square family.

Accordingly Gate 5 stays at global maturity `10/18` with zero complete blocks,
and the complete composite-gate count remains `0/5`.

## 5. Shortest next route

Assemble the 96 stationary faces and 32 terminal-preimage components into one
shared base-R1 subdivision/incidence quotient, then lift this exact engine to
depth two and arbitrary finite rank paths.  In parallel, attack F14/F15/F17 on
the now-numeric F10/F13/F16 component rows; those operator fields, not base-R1
family enumeration, are now the shortest Gate-5 obstruction.
