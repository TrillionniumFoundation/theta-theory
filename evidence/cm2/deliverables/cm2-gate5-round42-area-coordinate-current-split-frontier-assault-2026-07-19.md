# CM2 Gate 5 Round-42 area-coordinate/current-split frontier assault

Date: 2026-07-19  
Verdict: **canonical area coordinates remove the moving target momentum
singularity but not the target-position `c^-3` loss; the raw coordinate route
cannot close arbitrary-`R_n` F10 from the known moment**

## 1. Exact area-coordinate split

Use the canonical momentum

```text
p=sin(phi),
dp=cos(phi)dphi,
R*cos(phi)dr dphi=R dr dp.
```

For a ray-circle hit,

```text
p_1=w/R_1.
```

When the relative centre has parameter velocity `eta e_x`, exact
differentiation gives

```text
|partial_s p_1|<=25/4,
partial_ss p_1=0,
|partial_rs p_1|<=625/16,
|partial_phi,s p_1|<=25/4.
```

Hence the target momentum component has dyadic parameter rank exponent zero.

The physical boundary position `r_1=R_1 theta_1` still satisfies only

```text
|partial_s r_1|<=75/(4c_1),
|partial_ss r_1|<=625/(16c_1^3),
|partial_xs r_1|<155625/(8c_1^3).
```

Thus the full F10 path exponent is not removed by the coordinate change.

## 2. Exact no-implication model

In flat area measure a grazing shell with `c=2^-B` has natural momentum
width comparable to `c^2`.  The probability law

```text
P(B=2k)=(15/16)*16^-k
```

has total mass one and

```text
sum P(B)*2^(3B/2)<infinity,
sum P(B)*2^(3B)=infinity.
```

Therefore neither area coordinates nor the known physical marginal moment

```text
integral 2^(3B/2)dmu_s<134217735/64
```

logically controls the residual `c^-3` target-position charge.  This is a
no-implication theorem, not a claim that the actual arbitrary physical path
diverges.

## 3. The surviving typed route

For an area-preserving regular branch `F_s`, a face
`A_s={G_s<0}`, and

```text
X_s=(partial_s F_s) composed with F_s^-1,
```

change variables before differentiating.  Distributionally,

```text
partial_s[1_{G_s<0}(h composed F_s^-1)]
=-delta(G_s) G_s,s (h composed F_s^-1)
 -1_{G_s<0} X_s dot grad(h composed F_s^-1).
```

The first term is the F10 moving-face seed.  The second belongs to the F13
moving-boundary current/two traces and F16 flux cost.  Since
`div_mu X_s=0` on each regular branch, this route can avoid differentiating
the complete pulled-back face twice in singular Birkhoff position
coordinates.

The identity is exact, but arbitrary-`R_n` F13 traces, F16 flux costs and
all-face reassembly remain unproved.  Gate-5 maturity therefore stays
`7/18`, with zero complete blocks.

## 4. Latest-technology audit

The arXiv API was checked on 2026-07-19.  The official snapshot remains

```text
2104.06947v3 / 2604.19671v2 / 2606.10155v1.
```

Keyword searches for moving-scatterer billiards and billiard linear response
returned no newer theorem directly supplying arbitrary-depth moving-face
F10/F13/F16 bounds.  The Eulerian area-current split is therefore the next
matched route; no unrelated moving-wall theorem is imported.

## 5. Strict boundary

```text
target momentum rank exponent zero:  CERTIFIED
target position c^-3 removed:        NO
current-split identity:              CERTIFIED_ALGEBRAIC
arbitrary-R_n F10/F13/F16:           NOT CERTIFIED
Gate-5 maturity:                     7/18 UNCHANGED
complete blocks:                     0
CM2:                                 NO-GO_FOR_CLAIM
```

## 6. Validation

The suite passes syntax, pinned dependencies, strict JSON and independent
exact replay.  It rejects `32/32` hostile mutations.  Both certificate and
verifier default modes exit `2` and preserve the `NO-GO_FOR_CLAIM` boundary.
