# CM2 Round121 — exact-seed three-leg recuts and child-local Gate5 F1–F6

Date: 2026-07-23  
Verdict: **VERIFIED one exact analytic `b` seed, 24 genuine actual children, and child-local Gate5 F1–F6 (`6/18`).**

## Result

Round121 materializes the first exact member of the Round120 grazing-domain
standard-Borel parent-W family.  On that one seed it constructs the source,
first-image and second-image adapted natural recuts, pulls all image cuts back
to the source, and installs full-key F1–F6 slots on every common-refinement
child.

The frozen certificate contains:

- `1` exact analytic `b` witness;
- `23` independently isolated internal pullback cuts;
- `26` materialized stage recuts, split as `1 + 7 + 18`;
- `24` positive-length common-refinement actual children;
- `24` child-refined homogeneous-subbranch IDs;
- `720` immutable full-key slots: `120` for each of F1–F6;
- `43/43` pinned upstream and helper artifacts;
- zero root, recut or slot residuals.

The scope is deliberately seed-local.  Rank-3 maturity on these 24 children
is `6/18`; F7–F18 remain uninstalled.  Global Gate5 remains `10/18`, the
complete 18-field block count remains `0`, and CM2 remains
`NO-GO_FOR_CLAIM`.

## Exact analytic parent-W seed

The seed lies in the certified BYPASS central-outer cell

```text
Round113 parent
round113-cell:08b7ca8449af5f6e8d4e3abce98803656664ed7ec957aba62406763b68b2fea6

Round117 operator cell
round117-operator-cell:dca0117235e58b6a0cbc8b9db55ed846b8f26939041fa7eaffd3b68184d54ae1
```

Its rational anchor is

```text
c0* = 1/16384
b3* = 3/65536.
```

Let `t*` be the unique root in the frozen Round112 enclosure of

```text
F_BYPASS(t,1/16384,3/65536) = 0.
```

The verifier proves a fixed negative `t` derivative with absolute value
strictly greater than `3`, opposite endpoint signs and a root bracket narrower
than `10^-220`.  With the canonical `G:W` angular lift,

```text
theta* = pi-arcsin(t*)
b*     = arccos(1/16384)-(36/25) theta*.
```

The exact seed ID hashes only the parent/operator IDs, rational anchor,
unique-root predicate and angular-lift ID:

```text
round121-exact-parent-W:41462c4f6815ad00fd5d4456e5c13885feeab5e8343b009b8872b72d15cf18c8
```

No Arb enclosure or decimal rendering participates in that identity.  The
Round31 compact-Q2 parent-W, time-2 atom and branch-rule namespaces are not
reused.

## Exact source cell

Put `delta=10^-90` and parameterize the source natural cell by `x in [0,1)`:

```text
phi0(x)   = arccos(1/16384)+(36/61) delta x
c0(x)     = cos(phi0(x))
theta0(x) = theta*+(25/61) delta x
t(x)      = sin(theta0(x))
b3(x)     = sqrt(-Delta3(t(x),c0(x)))/(4/25).
```

The coefficient identity

```text
(36/61) = 4(9/25)(25/61)
```

proves `phi0-4(9/25)theta0=b*` on the whole cell.  Since the source adapted
density is `25/9+4=61/9`,

```text
u0(x) = delta x
```

holds exactly.  The verifier independently proves that `c0` and `b3` are
strictly decreasing, the whole source cell stays in
`H0_CENTRAL_OUTER`, and the Round113 owner, path and chart data remain fixed.

The official owners are

```text
W[-1,-1], G[0,0], G[-1,-2]
```

with selected collision charts `N,S,N` and roof counts `2,1,2`.  The
designated BYPASS coordinate belongs to `W[-1,-2]`, but the actual third
collision owner is `G[-1,-2]`; `b3` is never used as a collision angle or
homogeneity index.

## Three-stage adapted recut

The three input stages are the source, its first image and its second image.
Their orientations are `+1,-1,+1`.  The two image adapted coordinates use
both the normal and momentum angles:

```text
a1 = Theta_N(n1)+asin(p1)   U1(x)=a1(0)-a1(x)
a2 = Theta_S(n2)+asin(p2)   U2(x)=a2(x)-a2(0).
```

The 2048-bit independent replay proves strict monotonicity and

```text
6  < U1(1)/delta < 7
17 < U2(1)/delta < 18.
```

Consequently the natural-cell census is exactly

```text
source       1
first image  7
second image 18
total        26.
```

There are six unique roots of `U1(x)=j delta` and seventeen unique roots of
`U2(x)=j delta`.  Their strict source order is

```text
S2:1, S2:2, S1:1, S2:3, S2:4, S2:5, S1:2,
S2:6, S2:7, S1:3, S2:8, S2:9, S2:10, S1:4,
S2:11, S2:12, S1:5, S2:13, S2:14, S2:15,
S1:6, S2:16, S2:17.
```

All 23 endpoint equations have independent dyadic brackets, derivative signs,
opposite face signs and uniqueness proofs.  Distinct source pullbacks are
separated by more than `1/200`, yielding exactly 24 positive-length common
intervals with ranks `0..23`.

## Boundary ownership

The source cell is `[0,1)`: its right endpoint is not the terminal cell of
the Borel fibre.  Both image parents inherit that open right endpoint.  Every
internal natural cut is owned by the cell on its right, and each common child
is half-open in source orientation.  Coincident artificial cuts use the
conjunction of all owner predicates.

The natural boundaries `c0=0` and `b3=0` remain in the singular ledger.  This
exact seed is strictly separated from them, and no regular child captures
either boundary.

## F1–F6 full-key binding

Each common child receives its own identity

```text
round121-refined-subbranch:
sha256(round117-cell, exact-seed, source-k=0, common-rank).
```

Round120 F1–F4 are restricted and rebound to that refined identity.  F5 and
F6 are installed only after every stage image is shown to lie inside one
materialized canonical adapted cell of length at most `delta`.

The inherited one-step bounds are

```text
F5: ||(DT)^-1||_* < 144000/180337
F6: osc(log J_*)  < 3/200000.
```

Restriction cannot enlarge either a pointwise inverse bound or an
oscillation bound.  Across the three collision legs this gives

```text
F5 path product < 2985984000000000/5864817765532753
F6 path sum     < 9/200000.
```

Transparent-wall roof levels are prefix/suffix factorizations of a collision
leg, not extra collisions, so they add no Jacobian factor.  They nevertheless
receive distinct immutable Gate5 slots.  With five roof levels per child, the
slot census is

```text
24 children x 5 roof levels x 6 fields = 720 slots.
```

Every slot key is exactly

```text
(official-word-key-id,
 refined-homogeneous-subbranch-id,
 roof-level-j,
 field-name).
```

## Independent verification

The verifier uses 2048-bit Arb arithmetic and imports neither the Round121
producer nor a shared Round121 mathematics helper.  It independently checks:

- all `43/43` byte pins and the R113/R117/R120 seed crosswalk;
- the anchor root, exact intercept, slope-four identity and source adapted
  density;
- whole-cell source membership, owner/candidate/path/chart replay and the
  actual BYPASS winner;
- both image adapted coordinates, orientations and length ratios;
- all `23` root equations, `26` stage recuts, `24` common children and
  `24` refined subbranches;
- all `720` full-key F1–F6 slots and the transparent-wall factorization;
- all nested digests, counts, residuals and strict nonclaims.

It rejects `79` uniquely labelled re-signed semantic mutations and `15`
strict-JSON mutations.  Two clean producer runs and two complete independent
verifier runs are byte-identical to the canonical artifacts.

## Strict nonclaims and next blocker

Round121 does not claim:

- numerical materialization or uniform ranking of the whole Round120
  Borel-`b` family;
- any Round31 compact-Q2 identifier or recut instance;
- F7–F18 on the 24 exact-seed children;
- a global Gate5 maturity increase or a complete 18-field block;
- an endpoint-inclusive physical collar, cross-trace union reach or
  whole-face atlas.

The next core step must either extend this exact materialization through the
cut-equality strata of the Borel family or pay the first missing child-local
field beyond F6.  Until then, the valid state is seed-local `6/18`, global
`10/18`, complete blocks `0`, and `NO-GO_FOR_CLAIM`.
