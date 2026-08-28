# CM2 Round 88: fixed-density `Reg_alpha` synthesis and official F14 frontier

Date: 2026-07-22 (Asia/Shanghai)

## Frozen conclusion

All 152 current finite-root packets admit a bounded synthesis of their fixed
collision-density profiles into the frozen strong standard-family source
completion.  This is a genuine `Reg_alpha`/canonical-chop theorem.

It is **not** the official F14 `regular_density_operator_cost`.  The map is
defined only on `ell^1(152)` coefficients multiplying one fixed profile per
packet; it does not act on arbitrary regular-density inputs and does not
construct the required branchwise prefix/suffix intertwiner.  Therefore:

```text
fixed-profile Reg_alpha synthesis:       CERTIFIED 152/152
official immutable F14 slots:            0
finite-root candidate-local maturity:    13/18 unchanged
global Gate 5:                            10/18, blocks 0
```

## Certified mathematical sublayer

Round87 gives the exact transverse disintegration

```text
dLambda(v)=m(v)dv/M,
rho_v=cos(4r+v)/(sqrt(17)*m(v)).
```

Every conditional curve has `dphi/dr=4`.  On the 152 source windows,
`|p|<=1/50`, while `kappa>=25/9`.  With

```text
dell_*=(kappa+4)|dr|,
```

one obtains

```text
|d_(ell_*) log rho_v|
 =4|tan(phi)|/(kappa+4)
 <36/2989
 <1/80.
```

For a canonical piece of adapted length at most `delta_*=10^-90<1`,

```text
|Delta log rho_v| <(1/80)*ell_*
                  <=(1/80)*ell_*^(1/3).
```

Thus every fixed conditional density lies far inside the frozen adapted
one-third density cone.  Restriction and conditional normalization add only
a curvewise constant to `log rho`, so the regularity mark is unchanged.

For each conditional curve, take `N=ceil(ell_*/delta_*)` equal
adapted-length pieces.  If `N>1`, every piece has length in
`(delta_*/2,delta_*]`; an already-short curve is retained.  The weighted
boundary bookkeeping is

```text
Z_after <= Z_before + 2/delta_*.
```

Together with the Round87 pre-chop bound, the fixed-profile synthesis cost is
strictly below

```text
2*10^90 + 4302.
```

The transverse mass is integrated before short-fibre normalization, so no
corner normalization divergence is hidden.

## Why F14 remains open

The frozen Gate-5 norm ledger explicitly has

```text
regular_density_prefix_suffix_intertwiner = false,
immutable_complete_return_word_operator_registry = false.
```

The Round88 map has domain

```text
ell^1(152) coefficients on one fixed normalized collision-density profile
per packet.
```

That finite profile span is not the arbitrary-input regular-density Banach
domain required by the official branch operator.  A codomain embedding does
not manufacture the missing prefix/suffix action.  The 152 deterministic
keys are therefore recorded only as proposed crosswalk keys; every
`immutable_F14_slot_id` remains `NOT_MATERIALIZED`.

The completed empty F10 slots are correctly pinned, but their value zero does
not pay or replace the missing F14 operator interface.

## Verification

The producer uses 512-bit Arb arithmetic.  The 1024-bit verifier independently
recomputes all 152 key chains, adapted regularity inequalities, canonical
constants, and proposed key digests.  It also pins and rechecks the frozen
false prefix/suffix interface.  It rejects:

- 13/13 semantic mutations;
- 19/19 upstream pin mutations;
- 4/4 strict-JSON attacks.

Producer and verifier cold replay byte-for-byte against the frozen JSON.

## Next lawful route

To install F14, extend the construction from the fixed collision-density
profile on each packet to the full frozen regular-density input space, and
prove the same-key homogeneous prefix/suffix pushforward/pullback bound in the
accepted recipient.  Only then may an immutable F14 slot be materialized and
F15 attacked for field credit.
