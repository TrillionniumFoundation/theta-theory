# CM2 Gates 3/4 Round-48 Borel survivor-kernel assault

Date: 2026-07-19  
Strict verdict: **fixed-parameter Borel parent/survivor subkernels and two
conditional clock theorems are certified.  A new long-leaf reduction isolates
the missing target-sensitive cover atlas.  Numeric `H_cover`, actual
`beta_Wdiag`, same-ID joint return and Gate 4 remain unproved.**

## 1. Fixed-parameter Borel kernels

For each fixed `|s|<=1/400` and finite rank depth, the Round-27/35 component
registry and collision-SRB disintegration define a standard-Borel parent
kernel on IDs

```text
(component-id, b, source-interval-rank, incidence-rank-path, short-cell-k).
```

Every frozen finite forward or reverse survivor predicate is Borel, so its
restriction gives Borel subkernels `K_sur^fw` and `K_sur^rev`.  They share the
same parent/restriction ID and parent mass, but their survivor sets are not
asserted equal.  Zero survivor mass is sent to cemetery and is never
normalised.

This closes the previously missing fixed-`s` measurable parent/survivor
kernel schema.  It does not supply a joint `(s,component)` atlas or a
measurable grouping of the leaf registry into whole canonical proper
families.

## 2. Corrected whole-family shell clock

Conditionally on such a standard-Borel outer kernel of whole proper families,
let `p` be parent mass, `h_sigma` the positive post-cut survivor mass, and
`k_sigma` its dyadic shell.  Including the terminal C24 test time `H`, the
per-orientation clock is

```text
C_sigma = H + 319590 + 1005*k_sigma.
```

At `eta=1/6030`, the pointwise shell estimate gives

```text
h_sigma*exp(C_sigma/6030)
 < p*(6/5)^(318+ceil(H/1005))*(3/5)^k_sigma.
```

After integration, the former safe `5/2` loss disappears.  The forward plus
reverse survivor-weighted moments cost two copies.  This Round-47 one-step
post-cut route does not add the 9148-step killed block; a route through the
Round-42 hereditary block would have to add it.

The common survivor intersection is also a Borel subkernel.  Its two ambient
clocks satisfy, at `eta_pair=1/12060`,

```text
integral h_cap*exp((C_fw+C_rev)/12060)
 < (6/5)^(318+ceil(H/1005))*integral p.
```

Those clocks recover the two ambient survivors separately.  The intersection
can shrink to an arbitrarily short family and need not remain proper, so this
is not a same-ID joint return or a collision-time `q` bound.

## 3. Long-leaf reduction for the missing cover

The proper-family constant is

```text
C_p = 4*10^90*360493663/358863.
```

For a normalised proper family, leaves of adapted length below `delta` have
total weight at most `delta*C_p`.  Choosing

```text
delta_long = 358863/(2883949304*10^90)
```

therefore leaves at least half of the family weight on longer leaves.  It is
now enough to construct one common terminal time and, on every such long leaf,
disjoint once-counted W-diagonal crossing parents of source fraction

```text
zeta_rect >= 460800/5197322039.
```

Then `(1/2)*zeta_rect` reaches the Round-47 threshold
`230400/5197322039`.  No existing registry supplies this target-sensitive
long-leaf atlas, so the actual strict lower bound on `beta_Wdiag` remains zero.

As a useful physical comparison, the eight pairwise-disjoint stationary
W-diagonal cores have collision-SRB mass

```text
mu_s(union) > 7/89375,
```

which exceeds the beta threshold by
`1214558021/35731589018125`.  This two-dimensional stationary mass is not the
terminal crossing-parent weight of every singular proper family and is not
used as beta.

A separate conditional mixing route also improves sharply when the same
eight-core union is used.  A global plateau bump can be chosen with

```text
mu_s(g_W) > 343/5720000,
||g_W||_C1 < 7801,
Delta_W = 343/5720000 - 21/111718750
        = 213703/3575000000.
```

Thus future numerical proper-family mixing constants `C_SF,theta_SF` would
give the explicit candidate

```text
H_W=max(0,1+ceil(log(7801*C_SF/Delta_W)/(-log(theta_SF)))).
```

Those constants are still absent, and this route produces direct C24
minorisation rather than the stronger W-diagonal crossing ledger.

## 4. Latest-tech audit

The official pages remain `1210.0011v4`, `2104.06947v3`,
`2604.19671v2`, and `2606.10155v1`.  The additional official preprint
`2604.25881v1` (Climenhaga--Day, *Every finite horizon Sinai billiard map has
a unique measure of maximal entropy*) contains a qualitative “sufficient
rectangles” mechanism: long leaves cross reference rectangles after a
uniform finite time.  Its time and crossing fraction come from compactness
and mixing and are not numerical, and its rectangle is not yet embedded in
the selected W-diagonal C24 target.  It therefore identifies the right atlas
architecture but does not close the present numeric interface.

## 5. Exact frontier

Still missing are:

- a materialised target-sensitive long-leaf cover and numeric `H_cover`;
- an actual positive `beta_Wdiag` with artificial-child de-duplication;
- the measurable whole-proper-family grouping joined to the leaf kernel;
- identical/common forward-reverse survivors or a proper common return;
- complete `C_fw`, `C_rev`, collision-time `q`, and strong cemetery.

Thus Gate 4 remains `NOT_CERTIFIED`; the global strict verdict remains
`0/5`, CM2 `NO-GO_FOR_CLAIM`.
