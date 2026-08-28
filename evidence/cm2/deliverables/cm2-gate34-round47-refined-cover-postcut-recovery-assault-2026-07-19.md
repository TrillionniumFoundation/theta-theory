# CM2 Gate 3/4 Round-47 refined cover and post-cut recovery assault

Date: 2026-07-19  
Verdict: **the extended-parent minorisation is repaired in the adapted metric,
and post-cut recovery is numerical for each orientation at whole-family
level.  The actual covering weight/time and the same-ID two-orientation join
remain open.**

## 1. Two inherited metric interfaces are corrected

Round 31 described natural source cells as Euclidean-arclength `10^-90`
intervals but assigned the same adapted-length upper bound without paying the
line-element conversion.  Round 47 replaces that source-cell rule by the
deterministic adapted coordinate

```text
u_*(r)=integral_(r0)^r (kappa+4) dt
```

and half-open `u_*` intervals of length at most `10^-90`.  This is the
adapted-arclength rule already required by the Round-28 F5/F6 registry; its
clipped endpoints are Borel in the canonical leaf data and the recut preserves
the full parent measure.

Round 45/46 also multiplied a Euclidean crossing-length fraction by the
adapted-density ratio `R_ext`.  That mixed-metric pair-hit number is not reused.
The replacement calculation uses the adapted line element throughout.

## 2. Best current conditional C24 minorisation

Choose a white-obstacle diagonal C24 core with
`p in [-1/50,1/50]`.  For a monotone extended parent,

```text
dell_*=(kappa+V)|dr|,
integral kappa dr <= 2*pi,
integral V dr = |Delta phi| < pi,
ell_*(parent) < 3*pi < 66/7.
```

The transverse core arc has

```text
ell_*(crossing) >= 2*asin(1/50) > 1/25.
```

Thus its adapted-length fraction is `>7/1650`.  Combining this with the
pinned and retyped density continuation

```text
R_ext < 400000000/399794003
```

gives the strict one-bundle hit fraction

```text
h_Wdiag > 2798558021/660000000000.
```

To beat the frozen hit target `21/111718750`, the weight of disjoint
white-diagonal-crossing extended-parent IDs at one common terminal collision
must satisfy

```text
beta_Wdiag >= 230400/5197322039.
```

`1/22557` is safe and `1/22558` is the first reciprocal failure.  Artificial
children of one extended parent are counted once.  This is a conditional
threshold: no numerical `H_cover` or actual `beta_Wdiag` is inferred.

## 3. Numerical post-cut return, with the correct scope

For one whole adapted canonical proper standard family `G`, replaying the
one-step C24-killed Growth inequality gives

```text
Z(H) <= Z1*Z(G),
Z1 = 18367592526/360493663,
P = Z1*C_p,
2^316 < P < 2^317,
```

where `H=O_s G` is the unnormalised surviving family.  If

```text
x=mass(H)/mass(G),
2^(-(k+1)) < x <= 2^(-k),
```

then

```text
Z(H)/mass(H) < 2^(318+k).
```

The closed Growth half-block therefore returns this whole family to the same
proper class after

```text
R_post(k)=1005*(318+k)=319590+1005*k
```

closed iterations.  The zero-mass output is absorbed and never normalised.
The result is familywise, not leafwise: a single arbitrarily short recut leaf
need not itself be proper.

The argument applies to forward and reverse orientations separately.  It does
not identify their killed survivor subsets, survivor fractions or dyadic
indices.  For an explicitly finite or countable discrete list of whole-family
inputs, it also gives the conditional shell lemma

```text
sum_k m_k*exp(R_post(k)/6030)
  < (5/2)*(6/5)^318*sum parent_mass.
```

The standard-Borel parent/survivor mass kernel needed to integrate this over
the full parameterised carrier is not yet certified.

## 4. Exact frontier

Certified in this suite:

- corrected adapted source-cell schema;
- adapted-metric white-diagonal conditional hit lower bound;
- exact sufficient `beta_Wdiag` threshold;
- per-orientation whole-family dyadic post-cut proper return;
- conditional finite/countable family shell lemma.

Still not certified:

- actual target-sensitive `H_cover` and `beta_Wdiag`;
- a standard-Borel parent/survivor mass disintegration;
- a common same-ID forward/reverse killed-survivor registry and joint clock;
- numerical `C_fw/C_rev/q` and strong cemetery;
- Gate 4.

